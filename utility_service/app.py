# utility_service/app.py
import os
import sys
import requests
import json
from flask import Flask, request, jsonify
from flasgger import Swagger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ENTITY_SERVICE_URL

app = Flask(__name__)
swagger_config = {
    "headers": [], "specs": [{"endpoint": 'apispec_1', "route": '/apispec_1.json', "rule_filter": lambda rule: True, "model_filter": lambda tag: True}],
    "static_url_path": "/flasgger_static", "swagger_ui": True, "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(f"Utility Service: Menerima permintaan pendaftaran dengan data: {json.dumps(data, indent=2)}")
    try:
        response = requests.post(f"{ENTITY_SERVICE_URL}/users", json=data)
        print(f"Utility Service: Mengirim data ke Entity Service. Respon: {response.status_code}")
        if response.status_code == 201:
            print(f"Utility Service: User {data['email']} berhasil didaftarkan.")
            return jsonify({"message": "User registered successfully"}), 201
        else:
            print(f"Utility Service: Gagal mendaftarkan user. Respon: {response.json()}")
            return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Utility Service: Tidak dapat terhubung ke Entity Service. Error: {e}")
        return jsonify({"error": "Failed to connect to Entity Service"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Utility Service: Menerima permintaan login dengan data: {json.dumps(data, indent=2)}")
    try:
        response = requests.get(f"{ENTITY_SERVICE_URL}/users", params={'email': data['email']})
        print(f"Utility Service: Meminta data user ke Entity Service. Respon: {response.status_code}")
        if response.status_code == 200:
            user = response.json()
            import hashlib
            hashed_input_password = hashlib.md5(data['password'].encode()).hexdigest()
            if hashed_input_password == user['password']:
                # --- PERBAIKAN KEY ---
                # Gunakan 'users_id' sesuai dengan respons dari Entity Service
                print(f"Utility Service: Login berhasil untuk user {data['email']}.")
                return jsonify({"message": "Login successful", "users_id": user['users_id'], "name": user['name']}), 200
            else:
                print(f"Utility Service: Login gagal. Password salah untuk {data['email']}.")
                return jsonify({"error": "Invalid email or password"}), 401
        elif response.status_code == 404:
            print(f"Utility Service: Login gagal. User {data['email']} tidak ditemukan.")
            return jsonify({"error": "User not found"}), 404
        else:
            return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Utility Service: Tidak dapat terhubung ke Entity Service. Error: {e}")
        return jsonify({"error": "Failed to connect to Entity Service"}), 500

@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.get_json()
    print(f"--- NOTIFIKASI DARI TASK SERVICE ---")
    print(f"Data Notifikasi: {json.dumps(data, indent=2)}")
    print(f"------------------------------------")
    return jsonify({"message": "Notification processed"}), 200

if __name__ == '__main__':
    print("Utility Service berjalan di port 8002")
    app.run(port=8002, debug=True)