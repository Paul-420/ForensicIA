import json
import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('logs.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method TEXT,
    url TEXT,
    query_parameters TEXT,
    headers TEXT,
    attack_type TEXT
)
''')

# Sauvegarder les modifications
conn.commit()

# Lire le fichier JSON
with open('test.json', 'r') as file:
    data = json.load(file)

# Insérer les données dans la base de données
for entry in data:
    method = entry['method']
    url = entry['url']
    query_parameters = json.dumps(entry['query_parameters'])  # Convertir les paramètres de requête en chaîne JSON
    headers = json.dumps(entry['headers'])  # Convertir les en-têtes en chaîne JSON
    attack_type = entry.get('attack_type', 'No attack')  # Utiliser 'No attack' par défaut si 'attack_type' n'est pas présent

    cursor.execute('''
    INSERT INTO logs (method, url, query_parameters, headers, attack_type)
    VALUES (?, ?, ?, ?, ?)
    ''', (method, url, query_parameters, headers, attack_type))

# Sauvegarder les modifications et fermer la connexion
conn.commit()
conn.close()