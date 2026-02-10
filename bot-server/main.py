import requests
import json
from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError

app = Flask(__name__)

# Docker Network üzerindeki servis adresleri
OLLAMA_URL = "http://ollama:11434/api/generate"
SCHEMA_SVC = "http://schema-server:5001/schema"
VALUES_SVC = "http://values-server:5002/values"

def call_ollama_jk(prompt, context):
    """AI modeline güncelleme komutunu gönderir."""
    system_msg = (
        f"You are a strict JSON configurator. Update the following configuration based on the user's request: '{prompt}'. "
        f"Current Values: {json.dumps(context)}. "
        "IMPORTANT: Return ONLY the raw JSON object. Do not include any text or explanations."
    )
    
    payload = {
        "model": "phi3", # RAM dostu model
        "prompt": system_msg,
        "stream": False,
        "format": "json"
    }
    
    response = requests.post(OLLAMA_URL, json=payload)
    response_data = response.json()
    return json.loads(response_data['response'])

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    user_prompt = data.get('prompt', '').lower()
    
    # Uygulama ismini tespit etme
    app_name = "chat" if "chat" in user_prompt else "matchmaking" if "matchmaking" in user_prompt else "tournament"
    
    try:
        # 1. Şema ve mevcut değerleri al
        schema = requests.get(f"{SCHEMA_SVC}/{app_name}").json()
        current_config = requests.get(f"{VALUES_SVC}/{app_name}").json()
        
        # 2. AI ile yeni değerleri oluştur
        updated_config = call_ollama_jk(user_prompt, current_config)
        
        # 3. Doğrulama yap
        validate(instance=updated_config, schema=schema)
        
        # 4. Kaydetmesi için values-server'a gönder
        save_request = requests.post(f"{VALUES_SVC}/{app_name}", json=updated_config)
        
        return jsonify({
            "status": "success",
            "detected_app": app_name,
            "updated_config": updated_config
        })

    except ValidationError as e:
        return jsonify({"status": "error", "type": "Schema Error", "message": e.message}), 400
    except Exception as e:
        return jsonify({"status": "error", "type": "System Error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)