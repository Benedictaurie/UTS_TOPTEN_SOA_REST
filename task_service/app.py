# task_service/app.py
import os
import sys
import json
import requests
from flask import Flask, request, jsonify
from flasgger import Swagger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ENTITY_SERVICE_URL, UTILITY_SERVICE_URL, MICRO_SERVICE_URL

app = Flask(__name__)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)

@app.route('/booking', methods=['POST'])
def process_booking():
    data = request.get_json()
    print("Task Service: Memulai proses booking...")
    print(f"Task Service: Data yang diterima: {json.dumps(data, indent=2)}")
    
    # 1. Cek ketersediaan paket via Micro Service (logika sederhana, asumsikan selalu tersedia untuk contoh ini)
    # Memanggil Micro Service di sini.
    # print("Task Service: (Asumsi) Paket tersedia. Melanjutkan proses.")
    try:
        print(f"Task Service: Mengecek ketersediaan paket via Micro Service...")
        availability_response = requests.get(
            f"{MICRO_SERVICE_URL}/is_available",
            params={
                'package_id': data['package_id'],
                'booking_type': data['booking_type']
            }
        )
        
        if availability_response.status_code == 200:
            availability_data = availability_response.json()
            
            if not availability_data['available']:
                print(f"Task Service: Paket TIDAK TERSEDIA. Pesan: {availability_data.get('message')}")
                return jsonify({
                    "error": "Package not available",
                    "message": availability_data.get('message')
                }), 400
            
            print("Task Service: ✅ Paket TERSEDIA. Melanjutkan proses booking...")
            
        else:
            print(f"Task Service: Gagal mengecek ketersediaan. Status: {availability_response.status_code}")
            return jsonify({
                "error": "Failed to check package availability",
                "details": availability_response.json().get('error')
            }), availability_response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"Task Service: Gagal menghubungi Micro Service. Error: {e}")
        return jsonify({"error": "Failed to connect to Availability Service"}), 500

    # 2. Buat booking via Entity Service (jika paket tersedia)
    try:
        print(f"Task Service: Mencoba menghubungi Entity Service di {ENTITY_SERVICE_URL}/booking")
        entity_response = requests.post(f"{ENTITY_SERVICE_URL}/booking", json=data)
        
        if entity_response.status_code == 201:
            result = entity_response.json()
            print(f"Task Service: Booking berhasil! Kode Booking: {result.get('booking_code')}. Mengirim notifikasi...")
            
            # 3. Kirim notifikasi via Utility Service
            notification_data = {
                "user_id": data['user_id'],
                "message": f"Booking Anda dengan kode {result.get('booking_code')} telah dibuat dan menunggu konfirmasi."
            }
            
            try:
                requests.post(f"{UTILITY_SERVICE_URL}/notify", json=notification_data)
                print("Task Service: Notifikasi berhasil dikirim.")
            except requests.exceptions.RequestException as e:
                print(f"Task Service: Warning - Gagal mengirim notifikasi: {e}")
                # Notifikasi gagal, tapi booking tetap sukses
            
            print("Task Service: Proses booking selesai.")
            return jsonify({
                "message": "Booking processed successfully", 
                "booking_code": result.get('booking_code')
            }), 201
            
        else:
            print(f"Task Service: Gagal membuat booking. Status: {entity_response.status_code}, Respon: {entity_response.text}")
            return jsonify(entity_response.json()), entity_response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"Task Service: Gagal menghubungi Entity Service. Error: {e}")
        return jsonify({"error": "Failed to connect to Entity Service"}), 500


@app.route('/review', methods=['POST'])
def process_review():
    """Memproses penambahan review"""
    data = request.get_json()
    print("Task Service: Memulai proses penambahan review...")
    print(f"Task Service: Data yang diterima: {json.dumps(data, indent=2)}")
    
    try:
        print(f"Task Service: Membuat review via Entity Service di {ENTITY_SERVICE_URL}/review")
        entity_response = requests.post(f"{ENTITY_SERVICE_URL}/review", json=data)
        
        if entity_response.status_code == 201:
            print("Task Service: Proses penambahan review selesai.")
            return jsonify({"message": "Review processed successfully"}), 201
        else:
            print(f"Task Service: Gagal membuat review. Status: {entity_response.status_code}")
            return jsonify(entity_response.json()), entity_response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"Task Service: Gagal menghubungi Entity Service. Error: {e}")
        return jsonify({"error": "Failed to connect to Entity Service"}), 500

if __name__ == '__main__':
    print("Task Service berjalan di port 8001")
    app.run(port=8001, debug=True)