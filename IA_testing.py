import pandas as pd
import json
from joblib import load

# Charger le modèle
model = load('forensic.pkl')

# Charger les colonnes utilisées lors de l'entraînement
with open('columns.json', 'r') as f:
    columns = json.load(f)

# Lire le fichier JSON
with open('test.json', 'r') as file:
    data = json.load(file)

# Préparer les nouvelles données
new_logs_list = []

for entry in data:
    method = entry['method']
    url = entry['url']
    query_parameters = '&'.join([f"{k}={v}" for k, v in entry['query_parameters'].items()])
    headers = entry['headers']['User-Agent']  # Extraire uniquement le User-Agent
    
    new_logs_list.append({
        'method': method,
        'url': url,
        'query_parameters': query_parameters,
        'headers': headers
    })

# Créer un DataFrame avec les nouvelles données
new_logs = pd.DataFrame(new_logs_list)

# Transformer les nouvelles données de la même manière que les données d'entraînement
new_logs = pd.get_dummies(new_logs, columns=['method', 'url', 'query_parameters', 'headers'])

# Aligner les colonnes des nouvelles données avec celles des données d'entraînement
new_logs = new_logs.reindex(columns=columns, fill_value=0)

# Faire des prédictions
predictions = model.predict(new_logs)

# Ajouter les prédictions aux logs pour affichage
new_logs['prediction'] = predictions
print(new_logs)