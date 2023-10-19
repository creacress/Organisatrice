import pandas as pd
import re
from tqdm import tqdm  # Importation de tqdm

# Fonction pour vérifier si une valeur est une heure
def is_hour(value):
    return bool(re.match(r"^[0-2]?[0-9]H[0-5][0-9]$", value))

# Fonction pour extraire le code Regate et l'établissement de la chaîne combinée
def extract_regate_and_establishment(val):
    regate_code = val.split()[0] if val and val[0].isdigit() else None
    establishment = " ".join(val.split()[1:]) if regate_code else None
    return regate_code, establishment

# Lire le fichier brut CSV
file_path = "brut_rule.csv"
data = pd.read_csv(file_path, sep=',', encoding='utf-8')  # Assurez-vous d'utiliser le bon délimiteur et encodage

# Mappage des rôles aux colonnes correspondantes
role_columns = {
    "Dépôt": ["Code Regate (Dépôt)", "Etablissement (Dépôt)", "Heure_1 (Dépôt)", "Heure_2 (Dépôt)"],
    "Traitement": ["Code Regate (Traitement)", "Etablissement (Traitement)", "Heure_1 (Traitement)", "Heure_2 (Traitement)"],
    "Dépôt et Traitement": ["Code Regate (Dépôt et Traitement)", "Etablissement (Dépôt et Traitement)", "Heure_1 (Dépôt et Traitement)", "Heure_2 (Dépôt et Traitement)"]
}

structured_data = []

# Itérer sur les numéros de contrat uniques en utilisant tqdm pour afficher la barre de progression
for contract in tqdm(data["no_contr"].unique(), desc="Traitement des contrats", ncols=100):
    contract_rows = data[data["no_contr"] == contract]
    row_data = {
        "no_contr": contract,
        "no_ver": contract_rows["no_ver"].iloc[0],
        "lb_srvce": contract_rows["lb_srvce"].iloc[0]
    }
    
    # Traiter les valeurs en fonction du rôle
    for role, columns in role_columns.items():
        role_row_idx = contract_rows.index[contract_rows["val_cri"] == role].tolist()
        if not role_row_idx:
            continue
        role_row_idx = role_row_idx[0]
        
        role_related_rows = contract_rows[contract_rows.index < role_row_idx]["val_cri"].tolist()
        
        if role_related_rows:
            regate_code, establishment = extract_regate_and_establishment(role_related_rows[0])
            row_data[columns[0]] = regate_code
            row_data[columns[1]] = establishment
        
            hour_values = [val for val in role_related_rows[1:] if is_hour(val)]
            for i, col in enumerate(columns[2:], start=0):
                row_data[col] = hour_values[i] if len(hour_values) > i else None
            
    structured_data.append(row_data)

# Convertir les données structurées en un DataFrame
result = pd.DataFrame(structured_data)

# Enregistrer le DataFrame dans un fichier CSV
result.to_csv("structured_rule.csv", sep=',', encoding='utf-8', index=False)  # Utilisez le même délimiteur et encodage que pour la lecture
