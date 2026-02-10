from flask import Flask, jsonify, abort, request
import json
import os

app = Flask(__name__)

# Docker Compose'da bağladığımız ortak veri yolu
DATA_PATH = "/app/data"

@app.route('/values/<app_name>', methods=['GET'])
def get_values(app_name):
    # Dosya ismini 'chat.value.json' formatında arar
    path = os.path.join(DATA_PATH, f"{app_name}.value.json")
    if not os.path.exists(path):
        return jsonify({"error": f"File not found at {path}"}), 404
    
    with open(path, 'r') as f:
        return jsonify(json.load(f))

@app.route('/values/<app_name>', methods=['POST'])
def update_values(app_name):
    path = os.path.join(DATA_PATH, f"{app_name}.value.json")
    new_data = request.json
    
    try:
        with open(path, 'w') as f:
            json.dump(new_data, f, indent=2)
        return jsonify({"message": "Saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)