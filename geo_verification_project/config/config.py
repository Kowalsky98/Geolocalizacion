# config/config.py
from services.directory_service import get_directories_from_api

API_URL = "https://pocket-base-production.up.railway.app/api/collections/paths/records"

DIRECTORIES = get_directories_from_api(API_URL)
