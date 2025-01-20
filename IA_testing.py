import pandas as pd
from joblib import load

# Charger le modèle
model = load('forensic.pkl')

# Exemple de nouvelles données à prédire
new_logs = pd.DataFrame({
    'ip_address': ['192.168.1.1', '10.0.0.1'],
    'user_agent': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'curl/7.68.0'],
    'url': ['/login', '/contact'],
    'http_method': ['GET', 'POST'],
    'query_parameters': ['id=123', "' OR 'a'='a"],
    'response_status': [200, 500],
    'sql_keywords_detected': [0, 1],
    'anomalous_patterns': [0, 1]
})

# Transformer les nouvelles données de la même manière que les données d'entraînement
new_logs['ip_seg1'] = new_logs['ip_address'].apply(lambda x: int(x.split('.')[0]))
new_logs['ip_seg2'] = new_logs['ip_address'].apply(lambda x: int(x.split('.')[1]))
new_logs['ip_seg3'] = new_logs['ip_address'].apply(lambda x: int(x.split('.')[2]))
new_logs['ip_seg4'] = new_logs['ip_address'].apply(lambda x: int(x.split('.')[3]))
new_logs = new_logs.drop(columns=['ip_address'])

new_logs = pd.get_dummies(new_logs, columns=['user_agent', 'url', 'http_method', 'query_parameters'])

# Charger les données d'entraînement pour obtenir les colonnes correctes
data = pd.read_csv('web_attack_logs.csv')
X = data[['response_status', 'sql_keywords_detected', 'anomalous_patterns', 'ip_address', 'user_agent', 'url', 'http_method', 'query_parameters']]
X['ip_seg1'] = X['ip_address'].apply(lambda x: int(x.split('.')[0]))
X['ip_seg2'] = X['ip_address'].apply(lambda x: int(x.split('.')[1]))
X['ip_seg3'] = X['ip_address'].apply(lambda x: int(x.split('.')[2]))
X['ip_seg4'] = X['ip_address'].apply(lambda x: int(x.split('.')[3]))
X = X.drop(columns=['ip_address'])
X = pd.get_dummies(X, columns=['user_agent', 'url', 'http_method', 'query_parameters'])

# Aligner les colonnes des nouvelles données avec celles des données d'entraînement
new_logs = new_logs.reindex(columns=X.columns, fill_value=0)

# Faire des prédictions
predictions = model.predict(new_logs)

# Ajouter les prédictions aux logs pour affichage
new_logs['prediction'] = predictions
print(new_logs)