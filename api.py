from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Endpoint pour récupérer les logs
@app.route('/api/logs', methods=['GET'])
def get_logs():
    conn = sqlite3.connect('InterfaceWeb/logs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    conn.close()
    logs = [dict(id=row[0], method=row[1], url=row[2], query_parameters=row[3], headers=row[4], body=row[5], attack_type=row[6]) for row in rows]
    return jsonify(logs)

# Endpoint pour supprimer les logs
@app.route('/clear_database', methods=['POST'])
def clear_logs():
    conn = sqlite3.connect('InterfaceWeb/logs.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
    return jsonify({'message': 'Database cleared successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)