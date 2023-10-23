import pandas as pd

def read_excel_with_notification(path):
    print("Reading Excel file. This might take a while...")
    df = pd.read_excel(path, engine="openpyxl")
    print("Excel file loaded successfully!")
    return df

def main():
    # Specify the path directly
    file_path = "DSI_clean.xlsx"
    df = read_excel_with_notification(file_path)
    
    # Define columns for each category
    all_cols = {
        "depot_traitement": [col for col in df.columns if "Dépôt et Traitement" in col],
        "traitement": [col for col in df.columns if "Traitement" in col and "Dépôt et Traitement" not in col],
        "depot": [col for col in df.columns if "Dépôt" in col and "Dépôt et Traitement" not in col]
    }
    other_cols = [col for col in df.columns if col not in (all_cols["depot_traitement"] + all_cols["traitement"] + all_cols["depot"])]
    
    # Extracting sub-tables for "Dépôt", "Traitement", and "Dépôt et Traitement"
    subtables = {
        "main": df[other_cols + ["no_ver"]],
        "depot": df[["no_contr", "no_ver"] + all_cols["depot"]],
        "traitement": df[["no_contr", "no_ver"] + all_cols["traitement"]],
        "depot_et_traitement": df[["no_contr", "no_ver"] + all_cols["depot_traitement"]]
    }
    
    # Save each table to separate Excel files
    for name, subtable in subtables.items():
        subtable.to_excel(f"{name}_table.xlsx", index=False)
    
    print("Files have been saved successfully!")

    # Free up memory
    del df

if __name__ == "__main__":
    main()
