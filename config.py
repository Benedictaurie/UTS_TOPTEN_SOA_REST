import os
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'topten_soa')

# Service URLs 
TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://localhost:8001")
UTILITY_SERVICE_URL = os.getenv("UTILITY_SERVICE_URL", "http://localhost:8002")
ENTITY_SERVICE_URL = os.getenv("ENTITY_SERVICE_URL", "http://localhost:8003")
MICRO_SERVICE_URL = os.getenv("MICRO_SERVICE_URL", "http://localhost:8004")