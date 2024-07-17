# services/geo_service.py
import requests

def get_geolocation(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    if response.status_code == 200:
        data = response.json()
        # ipinfo.io devuelve la ubicación en un solo campo llamado 'loc'
        loc = data['loc'].split(',')
        latitude = float(loc[0])
        longitude = float(loc[1])
        return latitude, longitude
    else:
        raise Exception("Error al obtener geolocalización")

def get_ip():
    response = requests.get("https://api.ipify.org?format=json")
    if response.status_code == 200:
        return response.json()["ip"]
    else:
        raise Exception("Error al obtener la IP")
