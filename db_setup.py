import json
import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('InterfaceWeb/logs.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT DEFAULT CURRENT_TIMESTAMP,
    method TEXT,
    url TEXT,
    query_parameters TEXT,
    headers TEXT,
    body TEXT,
    attack_type TEXT
)
''')

# Sauvegarder les modifications
conn.commit()

# Lire le fichier JSON
with open('test2.json', 'r') as file:
    data = json.load(file)

# Insérer les données dans la base de données
for entry in data:
    time = entry['time']
    method = entry['method']
    url = entry['url']
    if method == "GET":
        query_parameters = json.dumps(entry.get('get', {}))  # Convertir les paramètres de requête en chaîne JSON
    elif method == "POST":
        query_parameters = json.dumps(entry.get('post', {}))  # Convertir les paramètres de requête en chaîne JSON
    else:
        query_parameters = json.dumps({})  # Par défaut, utiliser une chaîne JSON vide si la méthode n'est ni GET ni POST
    headers = json.dumps(entry['headers'])  # Convertir les en-têtes en chaîne JSON
    body = entry['body']
    attack_type = entry.get('attack_type', 'Not predicted')  # Utiliser 'Not predicted' par défaut si 'attack_type' n'est pas présent

    cursor.execute('''
    INSERT INTO logs (time, method, url, query_parameters, headers, body, attack_type)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (time, method, url, query_parameters, headers, body, attack_type))

# Sauvegarder les modifications et fermer la connexion
conn.commit()
conn.close()