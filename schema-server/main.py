from flask import Flask, jsonify, abort
import json
import os

app = Flask(__name__)

# Docker Compose'da bağladığımız ortak veri yolu (ReadOnly olarak kullanılabilir)
DATA_PATH = "/app/data"

@app.route('/schema/<app_name>', methods=['GET'])
def get_schema(app_name):
    # Dosya ismini 'chat.schema.json' formatında arar
    path = os.path.join(DATA_PATH, f"{app_name}.schema.json")
    
    if not os.path.exists(path):
        # Dosya yoksa 404 hatası döner
        return jsonify({"error": f"Schema file not found at {path}"}), 404
    
    try:
        with open(path, 'r') as f:
            schema_data = json.load(f)
            return jsonify(schema_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Servisi 5001 portunda başlatıyoruz
    app.run(host='0.0.0.0', port=5001)