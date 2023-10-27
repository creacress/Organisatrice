import pandas as pd

# Étape 1: Charger les fichiers
df_etablissement = pd.read_excel("Liste_Etablissements.xlsx")
df_dsi = pd.read_excel("count_dsi_trier_V2.xlsx")

# Création d'un dictionnaire pour faciliter la recherche
dict_etablissement = df_etablissement.set_index('Code Regate').to_dict(orient='index')

# Étape 3 & 4: Comparer et ajouter les résultats
for col in df_dsi.columns:
    if "Code Regate" in col:
        result_col_name = f"Resultat_{col}"  # Concaténation du nom de la colonne actuelle
        ouvert_col_name = f"Ouvert_{col}"

        def apply_logic(code):
            if pd.isna(code):
                return "", ""
            if code in dict_etablissement:
                site_traitement = dict_etablissement[code]["Site traitement Oui/Non"]
                ouvert_status = dict_etablissement[code]["Ouvert Oui/Non"]
                
                # Détermine le résultat en fonction de site_traitement
                if site_traitement == "Oui":
                    result = "Correspondance / Traitement"
                elif site_traitement == "Non":
                    result = "Non Traitement"
                else:
                    result = "Correspondance"
                
                ouvert = "Ouvert" if ouvert_status == "Oui" else "Fermé"
                return result, ouvert
            return "Non correspondance", ""

        df_dsi[result_col_name], df_dsi[ouvert_col_name] = zip(*df_dsi[col].map(apply_logic))

# Étape 6: Sauvegarder les modifications dans le même fichier
df_dsi.to_excel("count_dsi_trier_V2_test.xlsx", index=False)
