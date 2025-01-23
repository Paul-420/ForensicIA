import pandas as pd
import json
from joblib import load

# Charger le modèle
model = load('forensic.pkl')

# Charger les colonnes utilisées lors de l'entraînement
with open('columns.json', 'r') as f:
    columns = json.load(f)

# Fonction pour détecter les mots-clés SQL
def detect_sql_keywords(query):
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION", "ALTER", "CREATE", "EXEC", "XP_"]
    return any(keyword in query.upper() for keyword in sql_keywords)

# Lire le fichier JSON
with open('test.json', 'r') as file:
    data = json.load(file)

# Extraire les informations pertinentes
method = data['method']
url = data['url']
query_parameters = '&'.join([f"{k}={v}" for k, v in data['query_parameters'].items()])
headers = json.dumps(data['headers'])  # Convertir les headers en chaîne JSON
#sql_keywords_detected = int(detect_sql_keywords(query_parameters))

# Créer un DataFrame avec les nouvelles données
new_logs = pd.DataFrame({
    'method': [method],
    'url': [url],
    'query_parameters': [query_parameters],
    'headers': [headers],
    #'sql_keywords_detected': [sql_keywords_detected]
})

# Transformer les nouvelles données de la même manière que les données d'entraînement
new_logs = pd.get_dummies(new_logs, columns=['method', 'url', 'query_parameters', 'headers'])

# Aligner les colonnes des nouvelles données avec celles des données d'entraînement
new_logs = new_logs.reindex(columns=columns, fill_value=0)

# Faire des prédictions
predictions = model.predict(new_logs)

# Ajouter les prédictions aux logs pour affichage
new_logs['prediction'] = predictions
print(new_logs)