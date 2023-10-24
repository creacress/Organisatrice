import pandas as pd
import re
from tqdm import tqdm

# Fonction pour vérifier si une valeur est une heure
def is_hour(value):
    return bool(re.match(r"^[0-2]?[0-9]H[0-5][0-9]$", value))

# Fonction pour générer des noms de colonnes dynamiques
def generate_column_names(role, count):
    suffix = f" {count}" if count > 1 else ""
    return [
        f"Code Regate ({role}{suffix})",
        f"Etablissement ({role}{suffix})",
        f"Heure_1 ({role}{suffix})",
        f"Heure_2 ({role}{suffix})"
    ]

# Fonction principale pour traiter les données du contrat
def process_contract_rows_v4(rows):
    data = {
        "no_contr": rows.iloc[0]["no_contr"],
        "no_ver": rows.iloc[0]["no_ver"],
        "lb_srvce": rows.iloc[0]["lb_srvce"]
    }

    role_counts = {"Dépôt": 0, "Traitement": 0, "Dépôt et Traitement": 0}
    depot_et_traitement_count = 0  # Count for "Dépôt et Traitement"
    traitement_count = 0  # Count for "Traitement"

    i = 0
    while i < len(rows):
        row = rows.iloc[i]
        if row["val_cri"] in role_counts:
            role_counts[row["val_cri"]] += 1
            columns = generate_column_names(row["val_cri"], role_counts[row["val_cri"]])

            # Update the counts based on the role
            if row["val_cri"] == "Dépôt et Traitement":
                depot_et_traitement_count += 1
            elif row["val_cri"] == "Traitement":
                traitement_count += 1

            hours = [None, None]
            establishment_info = [None, None]

            if i - 1 >= 0 and is_hour(rows.iloc[i-1]["val_cri"]):
                hours[0] = rows.iloc[i-1]["val_cri"]
                if i - 2 >= 0 and is_hour(rows.iloc[i-2]["val_cri"]):
                    hours[1] = rows.iloc[i-2]["val_cri"]
                    establishment_info = (rows.iloc[i-3]["val_cri"].split(maxsplit=1) if i-3 >= 0 else [None, None])
                else:
                    establishment_info = (rows.iloc[i-2]["val_cri"].split(maxsplit=1) if i-2 >= 0 else [None, None])
            else:
                establishment_info = (rows.iloc[i-1]["val_cri"].split(maxsplit=1) if i-1 >= 0 else [None, None])

            data.update({
                columns[0]: establishment_info[0],
                columns[1]: establishment_info[1] if len(establishment_info) > 1 else None,
                columns[2]: hours[0],
                columns[3]: hours[1]
            })

        i += 1

    # Add the counts to the data
    data["Dépôt et Traitement Count"] = depot_et_traitement_count
    data["Traitement Count"] = traitement_count

    return data

# Lire les données CSV
file_path = "brut_rule.csv"
df = pd.read_csv(file_path, sep=',', encoding='utf-8')

# Préparation pour le traitement des données
result_data = []

# Traiter chaque contrat en utilisant groupby
for _, group in tqdm(df.groupby("no_contr"), desc="Traitement des contrats"):
    processed_data = process_contract_rows_v4(group)
    result_data.append(processed_data)

# Créer un DataFrame à partir des données traitées
result_df = pd.DataFrame(result_data)

# Enregistrer les résultats dans un fichier Excel
result_df.to_excel('test_count_dsi.xlsx', index=False, engine='openpyxl')
