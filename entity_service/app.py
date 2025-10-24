# entity_service/app.py
import os
import sys
import json
import random
import string
from flask import Flask, request, jsonify
from flasgger import Swagger
import mysql.connector
from mysql.connector import Error


# Tambahkan path folder induk ke sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Import semua model
from users import User
from tour_packages import TourPackage
from activity_package import ActivityPackage
from rental_packages import RentalPackage
from booking import Booking
from review import Review

app = Flask(__name__)
swagger_config = {
    "headers": [], "specs": [{"endpoint": 'apispec_1', "route": '/apispec_1.json', "rule_filter": lambda rule: True, "model_filter": lambda tag: True}],
    "static_url_path": "/flasgger_static", "swagger_ui": True, "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)

def get_db_connection():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        print("Entity Service: Berhasil terhubung ke database.")
        return conn
    except Error as e:
        print(f"Entity Service: Error connecting to MySQL Database: {e}")
        return None

# --- CRUD untuk Users ---
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    print(f"Entity Service: Menerima data untuk membuat user baru: {json.dumps(data, indent=2)}")
    user = User(users_id=None, **data)
    user.set_password(data['password'])
    
    conn = get_db_connection()
    if conn is None: return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (name, email, password, phone_number) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user.name, user.email, user.password, user.phone_number))
        conn.commit()
        print(f"Entity Service: User {user.email} berhasil dibuat.")
        return jsonify({"message": "User created successfully"}), 201
    except Error as e:
        print(f"Entity Service: Error creating user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users', methods=['GET'])
def get_user_by_email():
    email = request.args.get('email')
    print(f"Entity Service: Menerima permintaan untuk user dengan email: {email}")
    conn = get_db_connection()
    if conn is None: return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        if user_data:
            print(f"Entity Service: Ditemukan user: {json.dumps(user_data, indent=2)}")
            return jsonify(user_data), 200
        else:
            print(f"Entity Service: User dengan email {email} tidak ditemukan.")
            return jsonify({"message": "User not found"}), 404
    except Error as e:
        print(f"Entity Service: Error fetching user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- CRUD untuk Tour Packages ---
@app.route('/tour_packages', methods=['GET'])
def get_all_tour_packages():
    print("Entity Service: Menerima permintaan untuk semua data tour_packages.")
    conn = get_db_connection()
    if conn is None: return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM tour_packages WHERE is_available = TRUE")
        packages_data = cursor.fetchall()
        packages = [TourPackage(**p).to_dict() for p in packages_data]
        print(f"Entity Service: Mengembalikan {len(packages)} paket tour.")
        return jsonify(packages), 200
    except Error as e:
        print(f"Entity Service: Error fetching tour packages: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- CRUD untuk Activity Packages ---
@app.route('/activity_packages', methods=['GET'])
def get_all_activity_packages():
    print("Entity Service: Menerima permintaan untuk semua data activity_packages.")
    conn = get_db_connection()
    if conn is None: return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM activity_packages WHERE is_available = TRUE") #paket is_available yg false tdk ditampilkan di halaman main menu client yg lihat paket activity
        packages_data = cursor.fetchall()
        packages = [ActivityPackage(**p).to_dict() for p in packages_data]
        print(f"Entity Service: Mengembalikan {len(packages)} paket activity.")
        return jsonify(packages), 200
    except Error as e:
        print(f"Entity Service: Error fetching activity packages: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- CRUD untuk Rental Packages ---
@app.route('/rental_packages', methods=['GET'])
def get_all_rental_packages():
    print("Entity Service: Menerima permintaan untuk semua data rental_packages.")
    conn = get_db_connection()
    if conn is None: return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM rental_packages WHERE is_available = TRUE")
        packages_data = cursor.fetchall()
        packages = [RentalPackage(**p).to_dict() for p in packages_data]
        print(f"Entity Service: Mengembalikan {len(packages)} paket rental.")
        return jsonify(packages), 200
    except Error as e:
        print(f"Entity Service: Error fetching rental packages: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- CRUD untuk Booking ---
@app.route('/booking', methods=['POST'])
def create_booking():
    data = request.get_json()
    print(f"Entity Service: Menerima data untuk membuat booking baru: {json.dumps(data, indent=2)}")
    
    booking_code = "BKG-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # --- PERBAIKAN: Berikan nilai default untuk 'status' ---
    # Ambil data dari payload, dan tambahkan 'status' yang tidak ada di payload
    booking_data = {
        "booking_id": None,
        "booking_code": booking_code,
        "status": 'pending',  # Nilai default
        "created_at": None,   # Akan diisi oleh database
        **data # Gabungkan dengan data dari client
    }

    # --- TAMBAHAN: Untuk debugging ---
    print(f"Entity Service: Data yang akan digunakan untuk membuat objek Booking: {json.dumps(booking_data, indent=2)}")
    
    conn = get_db_connection()
    if conn is None: return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    try:
        # Gunakan booking_data yang sudah lengkap
        booking = Booking(**booking_data)
        query = """INSERT INTO booking 
                   (booking_code, user_id, package_id, booking_type, start_date, end_date, num_persons, total_price) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (booking.booking_code, booking.user_id, booking.package_id, 
                  booking.booking_type, booking.start_date, booking.end_date, 
                  booking.num_persons, booking.total_price)
        
        # --- TAMBAHAN: Untuk debugging ---
        print(f"Entity Service: Menjalankan query: {query}")
        print(f"Entity Service: Dengan parameter: {params}")

        cursor.execute(query, params)
        conn.commit()
        print(f"Entity Service: Booking dengan kode {booking_code} berhasil dibuat.")
        return jsonify({"message": "Booking created successfully", "booking_code": booking_code}), 201
    except Error as e:
        print(f"Entity Service: Error creating booking: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# GET booking by user
@app.route('/bookings', methods=['GET'])
def get_bookings_by_user():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
        
    print(f"Entity Service: Menerima permintaan untuk booking milik user_id: {user_id}")
    conn = get_db_connection()
    if conn is None: return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM booking WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        bookings_data = cursor.fetchall()
        print(f"Entity Service: Mengembalikan {len(bookings_data)} booking.")
        return jsonify(bookings_data), 200
    except Error as e:
        print(f"Entity Service: Error fetching bookings: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- CRUD untuk Review ---
@app.route('/review', methods=['POST'])
def create_review():
    data = request.get_json()
    print(f"Entity Service: Menerima data untuk membuat review baru: {json.dumps(data, indent=2)}")
    
    # --- PERBAIKAN KRUSIAL: Lengkapi data sebelum membuat objek ---
    # Ambil data dari payload, dan tambahkan parameter yang hilang
    review_data = {
        "review_id": None,
        "created_at": None,  # Nilai default, akan diisi oleh database
        **data # Gabungkan dengan data dari client
    }
    
    # --- TAMBAHAN: Untuk debugging ---
    print(f"Entity Service: Data yang akan digunakan untuk membuat objek Review: {json.dumps(review_data, indent=2)}")

    conn = get_db_connection()
    if conn is None: return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    try:
        review = Review(**review_data) 
        
        query = "INSERT INTO review (user_id, booking_id, rating, comment) VALUES (%s, %s, %s, %s)"
        params = (review.user_id, review.booking_id, review.rating, review.comment)
        
        # --- TAMBAHAN: Untuk debugging ---
        print(f"Entity Service: Menjalankan query: {query}")
        print(f"Entity Service: Dengan parameter: {params}")

        cursor.execute(query, params)
        conn.commit()
        print(f"Entity Service: Review untuk user_id {review.user_id} berhasil dibuat.")
        return jsonify({"message": "Review created successfully"}), 201
    except Error as e:
        print(f"Entity Service: Error creating review: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("Entity Service berjalan di port 8003")
    app.run(port=8003, debug=True)