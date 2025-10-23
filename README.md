# TOPTEN BALI TOUR - SOA REST API

## Deskripsi Layanan

1.  **Entity Service (Port 8003)**
    -   **Tanggung Jawab:** Sumber utama data (CRUD - Create, Read, Update, Delete) untuk semua entitas (`users`, `tour_packages`, `activity_packages`, `rental_packages`, `booking`, `review`).

2.  **Utility Service (Port 8002)**
    -   **Tanggung Jawab:** Menangani fungsi pendukung seperti autentikasi pengguna (login/register) dan simulasi notifikasi.

3.  **Task Service (Port 8001)**
    -   **Tanggung Jawab:** Mengelola alur proses bisnis yang kompleks. Sebagai orkestrator yang mengkoordinasikan panggilan ke layanan lain untuk proses booking dan review.

4.  **Micro Service (Port 8004)**
    -   **Tanggung Jawab:** Menyediakan fungsi-fungsi kecil dan spesifik, seperti pengecekan ketersediaan paket (`is_available`).

## 🛠️ Requirements
- Flask
- Flasgger
- python-dotenv
- mysql-connector-python
- requests
- PyJWT

## 🚀 Instalasi & Konfigurasi

### 1. Kloning Repository

```
git clone https://github.com/Benedictaurie/UTS_TOPTEN_SOA_REST.git
cd UTS_TOPTEN_SOA_REST
```

### 2. Cara menjalankan Aplikasi
- Membuka 4 terminal yang berbeda
- Di setiap terminal, navigasi ke folder layanan yang berbeda

**Terminal 1 - entity_service**
- `cd entity_service`
- `python app.py`

**Terminal 2 - utility_service**
- `cd utility_service`
- `python app.py`

**Terminal 3 - task_service**
- `cd task_service`
- `python app.py`

**Terminal 4 - micro_service**
- `cd micro_service`
- `python app.py`

**Terminal 5 - client.py**
- `cd direktori project`
- `python client.py`