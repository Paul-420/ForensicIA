import pandas as pd
import json
import sqlite3
from joblib import load

# Charger le modèle
model = load('forensic.pkl')

# Charger les colonnes utilisées lors de l'entraînement
with open('columns.json', 'r') as f:
    columns = json.load(f)

# Fonction pour détecter les mots-clés SQL
def detect_sql_keywords(query):
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION", "ALTER", "CREATE", "EXEC", "XP_", " OR "]
    return any(keyword in query.upper() for keyword in sql_keywords)

# Fonction pour détecter les mots-clés HTML
def detect_html_keywords(query):
    html_keywords = ["<script>", "<img>", "<div>", "<h1>", "<b>", "<i>", "<span>"]
    return any(keyword in query.lower() for keyword in html_keywords)

# Extraire les valeurs des query_parameters
def extract_values(query_parameters):
    if isinstance(query_parameters, dict):
        return ' '.join(query_parameters.values())
    return ''

# Connexion à la base de données
conn = sqlite3.connect('InterfaceWeb/logs.db')
cursor = conn.cursor()

# Lire les données depuis la base de données
cursor.execute("SELECT id, method, url, query_parameters, headers, body FROM logs")
rows = cursor.fetchall()

# Préparer les nouvelles données
new_logs_list = []

for row in rows:
    id, method, url, query_parameters, headers, body = row
    query_parameters = json.loads(query_parameters)  # Convertir les paramètres de requête en dict
    headers = json.loads(headers)  # Convertir les en-têtes en dict
    query_parameters_values = extract_values(query_parameters)  # Extraire les valeurs des paramètres de requête
    sql_keywords_detected = int(detect_sql_keywords(query_parameters_values))
    html_keywords_detected = int(detect_html_keywords(query_parameters_values))
    
    new_logs_list.append({
        'id': id,
        'method': method,
        'url': url,
        'query_parameters_values': query_parameters_values,
        'sql_keywords_detected': sql_keywords_detected,
        'html_keywords_detected': html_keywords_detected,
        'body': body
    })

# Créer un DataFrame avec les nouvelles données
new_logs = pd.DataFrame(new_logs_list)

# Convertir les colonnes booléennes en entiers
new_logs.loc[:, 'sql_keywords_detected'] = new_logs['sql_keywords_detected'].astype(int)
new_logs.loc[:, 'html_keywords_detected'] = new_logs['html_keywords_detected'].astype(int)

# Conserver la colonne 'id' avant de transformer les données
ids = new_logs['id']

# Vérifier si la colonne 'body' existe avant de la supprimer et de l'encoder
columns_to_drop = ['id']
columns_to_encode = ['method', 'url', 'query_parameters_values']

if 'body' in new_logs.columns:
    columns_to_encode.append('body')

# Transformer les nouvelles données de la même manière que les données d'entraînement
new_logs_transformed = pd.get_dummies(new_logs.drop(columns=columns_to_drop), columns=columns_to_encode)

# Aligner les colonnes des nouvelles données avec celles des données d'entraînement
new_logs_transformed = new_logs_transformed.reindex(columns=columns, fill_value=0)

# Faire des prédictions
predictions = model.predict(new_logs_transformed)

# Ajouter les prédictions aux logs pour affichage
new_logs['prediction'] = predictions

# Mettre à jour la base de données avec les prédictions
for i, row in new_logs.iterrows():
    cursor.execute("UPDATE logs SET attack_type = ? WHERE id = ?",
                   (row['prediction'], row['id']))

# Sauvegarder les modifications et fermer la connexion
conn.commit()
conn.close()

print(new_logs)