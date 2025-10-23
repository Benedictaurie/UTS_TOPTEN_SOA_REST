# micro_service/app.py
import os
import sys
import requests
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

@app.route('/is_available', methods=['GET'])
def is_package_available():
    package_id = request.args.get('package_id')
    booking_type = request.args.get('booking_type')
    
    print(f"Micro Service: Memeriksa ketersediaan untuk {booking_type}_package ID {package_id}")
    
    if not all([package_id, booking_type]):
        return jsonify({"error": "package_id and package_type are required"}), 400

    try:
        # 1. URL Endpoint Dibangun Secara Dinamis
        service_url = f"{ENTITY_SERVICE_URL}/{booking_type}_packages?include_unavailable=true"
        # Jika booking_type='tour'  -> URL menjadi /tour_packages
        # Jika booking_type='activity' -> URL menjadi /activity_packages
        # Jika booking_type='rental' -> URL menjadi /rental_packages
        response = requests.get(service_url)
        
        if response.status_code == 200:
            packages = response.json()
            # --- PERBAIKAN KEY ---
            # Cari paket dengan key yang benar (misal: 'tour_packages_id')
            id_key = f"{booking_type}_package_id"
            # Jika booking_type='tour'  -> id_key menjadi 'tour_packages_id'
            # Jika booking_type='activity' -> id_key menjadi 'activity_package_id'
            # Jika booking_type='rental' -> id_key menjadi 'rental_packages_id'
            package = next((p for p in packages if p[id_key] == int(package_id)), None)
            
            if package:
                if package['is_available']:
                    print(f"Micro Service: Paket {booking_type} ID {package_id} TERSEDIA.")
                    return jsonify({"available": True, "package": package}), 200
                else:
                    print(f"Micro Service: Paket {booking_type} ID {package_id} TIDAK TERSEDIA.")
                    return jsonify({"available": False, "message": "Package is not available"}), 200
            else:
                print(f"Micro Service: Paket {booking_type} ID {package_id} tidak ditemukan.")
                return jsonify({"available": False, "message": "Package not found"}), 404
        else:
            print(f"Micro Service: Gagal menghubungi Entity Service. Status: {response.status_code}")
            return jsonify({"error": "Failed to fetch package data"}), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Micro Service: Tidak dapat terhubung ke Entity Service. Error: {e}")
        return jsonify({"error": "Failed to connect to Entity Service"}), 500

if __name__ == '__main__':
    print("Micro Service berjalan di port 8004")
    app.run(port=8004, debug=True)