import pandas as pd
import random

# Générer des adresses IP aléatoires
def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Générer des user-agents aléatoires
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "curl/7.68.0",  # Fréquemment utilisé dans des attaques automatisées
    "python-requests/2.25.1"
]

# Générer des URLs et des paramètres
normal_urls = ["/home", "/login", "/search", "/products", "/contact"]
malicious_queries = [
    "' OR 1=1--",
    "' UNION SELECT username, password FROM users--",
    "DROP TABLE users;",
    "'; EXEC xp_cmdshell('whoami')--",
    "' OR 'a'='a",
    "' AND sleep(5)--"
]

# Générer des données normales et malveillantes
data = []
for _ in range(1000):
    # Type de requête : normale ou attaque
    is_attack = random.choices([0, 1], weights=[80, 20])[0]  # 20% de requêtes malveillantes

    ip_address = generate_ip()
    user_agent = random.choice(user_agents)
    http_method = random.choice(["GET", "POST"])
    url = random.choice(normal_urls)

    if is_attack:
        query_parameters = random.choice(malicious_queries)
        sql_keywords_detected = sum(1 for keyword in ["SELECT", "DROP", "UNION", "OR", "AND"] if keyword in query_parameters.upper())
        anomalous_patterns = 1  # Requête malveillante
    else:
        query_parameters = f"id={random.randint(1, 1000)}"
        sql_keywords_detected = 0
        anomalous_patterns = 0  # Requête normale

    response_status = random.choice([200, 404, 500]) if is_attack else 200

    data.append({
        "ip_address": ip_address,
        "user_agent": user_agent,
        "url": url,
        "http_method": http_method,
        "query_parameters": query_parameters,
        "response_status": response_status,
        "sql_keywords_detected": sql_keywords_detected,
        "anomalous_patterns": anomalous_patterns,
        "is_attack": is_attack
    })

# Créer un DataFrame
df = pd.DataFrame(data)

# Afficher un aperçu des données
print(df.head())

# Sauvegarder les données pour une utilisation ultérieure
df.to_csv("web_attack_logs.csv", index=False)
