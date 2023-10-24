---

# Scripts de traitement des données de contrat

Ce répertoire contient deux scripts Python essentiels pour le traitement et la structuration des données de contrat.

## 1. Structuration des données (`XXX_xxx.csv` -> `structured_data.xlsx`)

Ce script prend en entrée un fichier CSV brut, `XXX_xxx.csv`, contenant des informations sur différents contrats. Il traite ces données pour extraire des informations spécifiques et les structurer de manière plus lisible.

**Caractéristiques principales** :

- Identification et comptage des rôles "Dépôt et Traitement" et "Traitement".
- Structuration des données en fonction des rôles et des heures associées.
- Exportation des données structurées dans un fichier Excel, `structured_data.xlsx`.

## 2. Division des données par rôle (`XXX_xxx.xlsx` -> Plusieurs fichiers Excel)

Après avoir obtenu les données structurées, ce script prend `XXX_xxx.xlsx` comme entrée et divise les données en fonction de leur rôle : "Dépôt", "Traitement", "Dépôt et Traitement".

**Caractéristiques principales** :

- Lecture du fichier Excel `XXX_xxx.xlsx`.
- Extraction des données en fonction de leur rôle.
- Sauvegarde des données extraites dans des fichiers Excel séparés pour chaque rôle : `mxx_table.xlsx`, `xxx_table.xlsx`, `xxx_table.xlsx`, et `xxx_table.xlsx`.

## Utilisation

1. Assurez-vous d'avoir les bibliothèques nécessaires installées : `pandas`, `openpyxl`, `re`, et `tqdm`.
2. Placez les données brutes dans `Xxx.csv`.
3. Exécutez le premier script pour structurer les données.
4. Placez le fichier `XXX_xx.xlsx` (résultant du premier script ou fourni séparément) dans le répertoire.
5. Exécutez le deuxième script pour diviser les données par rôle.

---
