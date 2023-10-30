import pandas as pd

# Charger le fichier Excel
chemin_fichier = 'count_dsi_trier_knime.xlsx'
data = pd.read_excel(chemin_fichier)

# 1. Identifier les Colonnes à Utiliser
depot_et_traitement_cols = [col for col in data.columns if "Dépôt et Traitement" in col and "Ouvert" in col]
depot_cols = [col for col in data.columns if "Dépôt" in col and "Ouvert" in col]

# 2. Compter "Dépôt et Traitement" et "Dépôt" en utilisant des opérations vectorisées
data["Dépôt et Traitement Count"] = (data[depot_et_traitement_cols] == "Ouvert").sum(axis=1)
data["Dépôt Count"] = (data[depot_et_traitement_cols + depot_cols] == "Ouvert").sum(axis=1)

# Enregistrer le DataFrame mis à jour dans le même fichier Excel
with pd.ExcelWriter(chemin_fichier, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    data.to_excel(writer, index=False)
