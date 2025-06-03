import json
import requests
from pymongo import MongoClient
from geopy.distance import geodesic
from collections import defaultdict

# --- Étape 1 : Télécharger les données JSON depuis data.gouv.fr ---
url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json?lang=fr&timezone=Europe%2FParis"

print("🔄 Téléchargement des données...")
response = requests.get(url)
response.raise_for_status()  # Arrête si erreur HTTP
data = response.json()  # Chargement en liste de dict

print(f"Nombre de stations reçues : {len(data)}")
json_formate = json.dumps(data, indent=4, ensure_ascii=False)
#print(json_formate)

# --- 2--- : Connexion MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["carburant_db"]
collection = db["stations"]
collection.delete_many({})  # On vide la collection pour repartir à zéro

# --- 3 ---- : Traitement et insertion des données ---
docs = []

for s in data:
    try:
        # Prix : parse JSON
        if not s.get("prix"):
            continue
        prix_list = []
        if isinstance(s["prix"], str):
            try:
                prix_list = json.loads(s["prix"])
            except json.JSONDecodeError:
                continue
        elif isinstance(s["prix"], list):
            prix_list = s["prix"]
        else:
            continue

        # Services
        services_list = []
        if "services" in s and s["services"]:
            if isinstance(s["services"], str):
                try:
                    services_list = json.loads(s["services"]).get("service", [])
                except json.JSONDecodeError:
                    services_list = []
            elif isinstance(s["services"], list):
                services_list = s["services"]
            else:
                services_list = []

        # Coordonnées (priorité au champ 'geom')
        if "geom" in s and s["geom"]:
            latitude = s["geom"].get("lat")
            longitude = s["geom"].get("lon")
        else:
            latitude = float(s.get("latitude", 0)) / 100000 if s.get("latitude") else None
            longitude = float(s.get("longitude", 0)) / 100000 if s.get("longitude") else None

        if latitude is None or longitude is None:
            continue  # Pas de coord => ignore la station

        ville = s.get("ville")
        adresse = s.get("adresse")
        # Construire document MongoDB la collection
        doc = {
            "id": s.get("id"),
            "ville": ville.title() if ville else "",
            "adresse": adresse.title() if adresse else "",
            "cp": s.get("cp"),
            "latitude": latitude,
            "longitude": longitude,
            "prix": [],
            "services": services_list,
        }

        # Ajouter des prix des différents carburants pour la station
        for p in prix_list:
            if isinstance(p, dict) and "@nom" in p and "@valeur" in p:
                try:
                    doc["prix"].append({
                        "nom": p["@nom"],
                        "valeur": float(p["@valeur"]),
                        "maj": p.get("@maj")
                    })
                except ValueError:
                    continue

        docs.append(doc)

    except Exception as e:
        print(f"Erreur avec une station : {e}")
        continue

collection.insert_many(docs)
print(f"✅ {len(docs)} stations insérées dans MongoDB.")

# ---4---Analyse autour d’un lieu donné ---
#reference_location = (46.839, 5.687)  # Latitude/longitude de Poligny (exemple)
reference_location = (48.7961, 2.3076)  # Bagneux

rayon_km = 10

stations_proches = []

for station in docs:
    try:
        location = (station["latitude"], station["longitude"])
        #Calcul distance avec geodesic
        distance_km = geodesic(reference_location, location).km
        if distance_km <= rayon_km:
            station["distance_km"] = round(distance_km, 2)
            stations_proches.append(station)
    except Exception:
        continue

print(f"\n📍 {len(stations_proches)} stations dans un rayon de {rayon_km} km autour du point donné.")

# ---5-- Calcul moyenne des prix par carburant à partir de la liste des station recupérer aux alentours---
#On crée une dictionnaire contenant les prix pour les differents carburants avec la bibliothèque defaultdict
prix_par_carburant = defaultdict(list)

for station in stations_proches:
    for p in station["prix"]:
        prix_par_carburant[p["nom"]].append(p["valeur"])

print("\n📊 Moyenne des prix par carburant dans la zone :")
for carburant, valeurs in prix_par_carburant.items():
    moyenne = sum(valeurs) / len(valeurs)
    print(f" - {carburant} : {moyenne:.3f} €/L")

# --- 6 ---- Affichage de quelques stations proches ---
print("\nExemples de stations proches :")
for station in stations_proches[:3]:
    print(f" - {station['ville']} ({station['distance_km']} km) - {station['adresse']}")
    for p in station["prix"]:
        print(f"     {p['nom']}: {p['valeur']} €/L (maj {p['maj']})")

# Supprimer les champs _id (non sérialisables en JSON)
for station in stations_proches:
    station.pop('_id', None)  # supprime la clé _id si elle existe

# Maintenant, écrire les données dans le fichier JSON
with open("stations_bagneux.json", "w", encoding="utf-8") as f:
    json.dump(stations_proches, f, ensure_ascii=False, indent=2)