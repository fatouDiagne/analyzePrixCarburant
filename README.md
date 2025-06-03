# 🚗 Analyse des Prix du Carburant autour de Bagneux

Ce projet a pour objectif d’analyser et de visualiser les prix des carburants dans un rayon de 10 km autour de la ville de **Bagneux** (France), à partir de données publiques. Il combine un **pipeline ETL en Python**, une **base MongoDB**, et une **visualisation interactive** avec **Leaflet.js**.

---

## 🗂️ Contenu du projet

- `analyze-data-carburant.py` : Script Python complet (ETL)  
- `stations_bagneux.json` : Résultat JSON des stations filtrées autour de Bagneux  
- `Visualisation-map.html` : Carte interactive avec Leaflet  
- `README.md` : Documentation du projet

---

## 🔍 Objectifs

- Extraire les données officielles des prix des carburants via [data.gouv.fr](https://data.economie.gouv.fr)
- Nettoyer, structurer et stocker les données dans MongoDB
- Filtrer les stations dans un rayon de 10 km autour de Bagneux
- Calculer les **moyennes de prix par type de carburant**
- Visualiser les stations proches sur une **carte interactive**

---

## ⚙️ Technologies utilisées

- **Python** (requests, json, geopy, pymongo)
- **MongoDB** (stockage des données structurées)
- **Leaflet.js** (carte interactive avec OpenStreetMap)
- **HTML/CSS** (interface web simple)


---

## 🧪 Lancer le projet

### 1. Lancer MongoDB en local

Assure-toi d’avoir MongoDB installé et en cours d’exécution.

### 2. Exécuter le script Python

```bash
python analyse_carburant.py
````


![Capture d'écran 2025-06-03 000107](https://github.com/user-attachments/assets/b7c5976d-d65a-48ee-bbe6-42ac9e827a8b)
![Capture d'écran 2025-06-03 000244](https://github.com/user-attachments/assets/af0b6bc8-8953-415c-84af-489212d11d59)
![Capture d'écran 2025-06-03 000338](https://github.com/user-attachments/assets/78655ed4-1b69-44ad-8d63-2312c742e64c)



