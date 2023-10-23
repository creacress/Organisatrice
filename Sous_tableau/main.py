import pandas as pd
from tqdm import tqdm

# Function to wrap pandas read_excel with tqdm for a progress bar using openpyxl engine
def read_excel_with_progress(path):
    with tqdm(total=100, desc="Reading Excel") as pbar:
        df = pd.read_excel(path, engine="openpyxl")
        pbar.update(100)
    return df

# Specify the path directly
file_path = "DSI_clean.xlsx"
df = read_excel_with_progress(file_path)

# Define columns for each category
depot_traitement_cols = [col for col in df.columns if "Dépôt et Traitement" in col]
traitement_cols = [col for col in df.columns if "Traitement" in col and "Dépôt et Traitement" not in col]
depot_cols = [col for col in df.columns if "Dépôt" in col and "Dépôt et Traitement" not in col]
other_cols = [col for col in df.columns if col not in depot_traitement_cols and col not in traitement_cols and col not in depot_cols]

# Extracting sub-tables for "Dépôt", "Traitement", and "Dépôt et Traitement"
depot_subtable = df[["no_contr"] + depot_cols]
traitement_subtable = df[["no_contr"] + traitement_cols]
depot_et_traitement_subtable = df[["no_contr"] + depot_traitement_cols]

# Cleaning up the main table by dropping the extracted columns
main_table = df[other_cols]

# Save each table to separate Excel files
main_table.to_excel("main_table.xlsx", index=False)
depot_subtable.to_excel("depot_subtable.xlsx", index=False)
traitement_subtable.to_excel("traitement_subtable.xlsx", index=False)
depot_et_traitement_subtable.to_excel("depot_et_traitement_subtable.xlsx", index=False)

print("Files have been saved successfully!")
