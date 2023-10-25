import pandas as pd

# 1. Charger les fichiers Excel.
depot_table = pd.read_excel("Dépôt.xlsx")
liste_etablissements = pd.read_excel("Liste_Etablissements.xlsx", usecols=["CodeREGATE"])

# 2. Convertir directement la série en un ensemble.
code_regate_set = set(liste_etablissements["CodeREGATE"].astype(str))

# 3. Approche vectorisée pour vérifier chaque colonne "Code Regate (Dépôt X)".
depot_columns = [col for col in depot_table.columns if "Code Regate" in col]
result_columns = []

for col in depot_columns:
    if not depot_table[col].isna().all():
        result_col_name = f"Résultat {col.split(' ')[-1]}"
        result_columns.append(result_col_name)
        
        mask_correspond = (~depot_table[col].isna()) & (depot_table[col].astype(str).isin(code_regate_set))
        mask_no_correspond = (~depot_table[col].isna()) & (~depot_table[col].astype(str).isin(code_regate_set))
        
        depot_table.loc[mask_correspond, result_col_name] = "Correspond"
        depot_table.loc[mask_no_correspond, result_col_name] = "Ne correspond pas"
        depot_table[result_col_name] = depot_table[result_col_name].where(~depot_table[col].isna(), other=None)

# Filtrer les colonnes à sauvegarder
cols_to_save = ['no_contr'] + depot_columns + [col.replace("Code Regate", "Etablissement") for col in depot_columns] + result_columns
filtered_depot_table = depot_table[cols_to_save]

# Division du dataframe en fonction des résultats
correspond_rows = filtered_depot_table[result_columns].eq("Correspond").any(axis=1)
correspond_df = filtered_depot_table[correspond_rows]
no_correspond_df = filtered_depot_table[~correspond_rows]

# Sauvegarde des dataframes dans différentes feuilles du même fichier Excel
with pd.ExcelWriter("chemin_vers_votre_fichier_de_resultats_optimized.xlsx") as writer:
    correspond_df.to_excel(writer, sheet_name="Correspond", index=False)
    no_correspond_df.to_excel(writer, sheet_name="Ne correspond pas", index=False)
