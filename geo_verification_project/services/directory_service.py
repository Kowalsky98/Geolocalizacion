# services/directory_service.py
import os
import requests

def get_directories_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        directories = [(item['path'].replace('\\\\', '\\'), item['isAllow']) for item in data['items']]
        return directories
    except requests.RequestException as e:
        raise Exception(f"Error al obtener directorios de la API: {e}")

def verify_directories(directories):
    invalid_directories = []
    for directory, is_allowed in directories:
        if not is_allowed and os.path.exists(directory):
            invalid_directories.append(directory)
    return invalid_directories

def check_missing_directories(directories):
    missing_directories = []
    for directory, is_allowed in directories:
        if is_allowed and not os.path.exists(directory):
            missing_directories.append(directory)
    return missing_directories
