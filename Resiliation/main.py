import pandas as pd

# Lire le fichier Excel
df = pd.read_excel('chemin_du_fichier.xlsx')

# Filtrer les lignes selon les critères
resultat = df[(df['Catégorie de Contrat'] == 'Contrat Simple') & (df['Statut Contrat'] == 'Inactif')]

# Sauvegarder le résultat dans un nouveau fichier Excel
resultat.to_excel('resultat.xlsx', index=False)
