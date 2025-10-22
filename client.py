# client.py
import requests
import os
import json
from config import UTILITY_SERVICE_URL, ENTITY_SERVICE_URL, TASK_SERVICE_URL

# Fungsi untuk membersihkan layar terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

current_user = None

def register():
    clear_screen()
    print("--- DAFTAR AKUN BARU ---")
    name = input("Nama: ")
    email = input("Email: ")
    password = input("Password: ")
    phone_number = input("No. HP (opsional): ")

    payload = {
        "name": name, 
        "email": email, 
        "password": password,
        "phone_number": phone_number
    }
    try:
        response = requests.post(f"{UTILITY_SERVICE_URL}/register", json=payload)
        print("\n[Respon Server]:")
        if response.status_code == 201:
            print("✅ Pendaftaran berhasil! Silakan login.")
        else:
            print(f"❌ Gagal mendaftar: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Tidak dapat terhubung ke layanan. {e}")
    input("\nTekan Enter untuk kembali ke menu utama...")


def login():
    global current_user
    clear_screen()
    print("--- LOGIN ---")
    email = input("Email: ")
    password = input("Password: ")

    payload = {"email": email, "password": password}
    try:
        response = requests.post(f"{UTILITY_SERVICE_URL}/login", json=payload)
        print("\n[Respon Server]:")
        if response.status_code == 200:
            current_user = response.json()
            print(f"✅ Login berhasil! Selamat datang, {current_user['name']}.")
        else:
            print(f"❌ Login gagal: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Tidak dapat terhubung ke layanan. {e}")
    input("\nTekan Enter untuk kembali ke menu utama...")


def view_packages():
    clear_screen()
    print("--- LIHAT PAKET YANG TERSEDIA ---")
    print("1. Paket Tour")
    print("2. Paket Activity")
    print("3. Paket Rental")
    choice = input("Pilih jenis paket (1-3): ")

    service_map = {
        "1": f"{ENTITY_SERVICE_URL}/tour_packages",
        "2": f"{ENTITY_SERVICE_URL}/activity_packages",
        "3": f"{ENTITY_SERVICE_URL}/rental_packages"
    }

    if choice in service_map:
        try:
            response = requests.get(service_map[choice])
            if response.status_code == 200:
                packages = response.json()
                if not packages:
                    print("Tidak ada paket yang tersedia.")
                else:
                    print(f"\n--- Daftar Paket ---")
                    for p in packages:
                        # --- PERBAIKAN: Tampilkan nama paket rental dengan benar ---
                        if choice == '3': # Untuk rental
                            package_name = f"{p['brand']} {p['model']}"
                            package_id = p['rental_packages_id']
                            package_price = p['price_per_day']
                            print(f"ID: {package_id} | Nama: {package_name} | Harga/Hari: {package_price}")
                        else: # Untuk tour dan activity
                            package_name = p['name']
                            package_id = p.get('tour_packages_id') or p.get('activity_package_id')
                            package_price = p.get('price') or p.get('price_per_person')
                            print(f"ID: {package_id} | Nama: {package_name} | Harga: {package_price}")
                            if choice == '1': # Cetak durasi hanya untuk tour
                                print(f"  Durasi: {p['duration_days']} hari")
                        
                        print(f"  Deskripsi: {p['description']}\n")
            else:
                print(f"❌ Gagal mengambil data paket. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: Tidak dapat terhubung ke layanan. {e}")
    else:
        print("Pilihan tidak valid.")
    input("\nTekan Enter untuk kembali ke menu utama...")


def make_booking():
    global current_user
    if not current_user:
        print("❌ Anda harus login terlebih dahulu!")
        input("Tekan Enter untuk kembali...")
        return

    clear_screen()
    print("--- BUAT BOOKING BARU ---")
    package_type = input("Tipe Paket (tour/activity/rental): ").lower()
    if package_type not in ['tour', 'activity', 'rental']:
        print("Tipe paket tidak valid.")
        input("Tekan Enter untuk kembali...")
        return
    
    try:
        id_key_map = {"tour": "tour_packages_id", "activity": "activity_package_id", "rental": "rental_packages_id"}
        package_id = int(input(f"ID Paket ({id_key_map[package_type]}): "))
        num_persons = int(input("Jumlah Orang: "))
        start_date = input("Tanggal Mulai (YYYY-MM-DD): ")
        end_date = input("Tanggal Selesai (YYYY-MM-DD, opsional): ") or None
        total_price = float(input("Total Harga (masukkan manual): "))

        payload = {
            "user_id": current_user['users_id'],
            "package_id": package_id,
            "booking_type": package_type,
            "start_date": start_date,
            "end_date": end_date,
            "num_persons": num_persons,
            "total_price": total_price
        }
        
        print(f"\nMengirim data booking: {json.dumps(payload, indent=2)}")
        response = requests.post(f"{TASK_SERVICE_URL}/booking", json=payload)
        print("\n[Respon Server]:")
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Booking berhasil! Kode Booking Anda: {result.get('booking_code')}")
        else:
            print(f"❌ Gagal membuat booking: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Tidak dapat terhubung ke layanan. {e}")
    except ValueError:
        print("❌ Input tidak valid. Pastikan ID dan jumlah orang berupa angka.")
    input("\nTekan Enter untuk kembali ke menu utama...")


def get_user_bookings():
    """Mengambil daftar booking untuk user yang sedang login."""
    try:
        # Kita butuh endpoint baru di entity service untuk ini
        response = requests.get(f"{ENTITY_SERVICE_URL}/bookings", params={'user_id': current_user['users_id']})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Gagal mengambil data booking. Status: {response.status_code}")
            print(f"   Respon Server: {response.json().get('error', 'Tidak ada pesan error.')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Tidak dapat terhubung ke layanan. {e}")
        return []

def write_review():
    global current_user
    if not current_user:
        print("❌ Anda harus login terlebih dahulu!")
        input("Tekan Enter untuk kembali...")
        return

    clear_screen()
    print("--- TULIS REVIEW ---")
    
    bookings = get_user_bookings()
    if not bookings:
        print("Anda belum memiliki booking yang bisa direview.")
        input("Tekan Enter untuk kembali...")
        return

    print("Pilih booking yang ingin Anda review:")
    for i, b in enumerate(bookings):
        print(f"{i+1}. Kode: {b['booking_code']} | Tipe: {b['booking_type']} | Status: {b['status']}")

    try:
        choice = int(input("Masukkan nomor booking: ")) - 1
        if not (0 <= choice < len(bookings)):
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk kembali...")
            return

        selected_booking = bookings[choice]
        if selected_booking['status'] != 'confirmed':
            print("❌ Hanya booking yang sudah dikonfirmasi yang bisa direview.")
            input("Tekan Enter untuk kembali...")
            return

        rating = int(input("Masukkan rating (1-5): "))
        if not (1 <= rating <= 5):
            print("Rating harus antara 1 dan 5.")
            input("Tekan Enter untuk kembali...")
            return
            
        comment = input("Masukkan komentar (opsional): ")

        payload = {
            "user_id": current_user['users_id'],
            "booking_id": selected_booking['booking_id'],
            "rating": rating,
            "comment": comment
        }
        print(f"\nMengirim data review: {json.dumps(payload, indent=2)}")

        # Panggil task service untuk proses review
        response = requests.post(f"{TASK_SERVICE_URL}/review", json=payload)
        print("\n[Respon Server]:")
        if response.status_code == 201:
            print("✅ Review berhasil ditambahkan!")
        else:
            print(f"❌ Gagal menambahkan review: {response.json().get('error', 'Unknown error')}")

    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"❌ Terjadi error: {e}")
    
    input("\nTekan Enter untuk kembali ke menu utama...")

def main_menu():
    global current_user
    while True:
        clear_screen()
        print("=== APLIKASI TOPTEN BALI TOUR ===")
        if current_user:
            print(f"Selamat datang, {current_user['name']}!")
        print("\n--- Menu Utama ---")
        print("1. Daftar Akun Baru")
        print("2. Login")
        if current_user:
            print("3. Lihat Paket")
            print("4. Buat Booking")
            print("5. Tulis Review") 
            print("6. Logout")
        else:
            print("3. Lihat Paket")
        print("0. Keluar")
        
        choice = input("Pilih menu: ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            view_packages()
        elif choice == '4' and current_user:
            make_booking()
        elif choice == '5' and current_user:
            write_review() 
        elif choice == '6' and current_user:
            current_user = None
            print("Anda telah logout.")
            input("Tekan Enter untuk melanjutkan...")
        elif choice == '0':
            print("Terima kasih telah menggunakan aplikasi ini!")
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk melanjutkan...")

if __name__ == '__main__':
    main_menu()