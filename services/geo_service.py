# services/geo_service.py
import requests

def get_ip_address():
    """Obtiene la dirección IP pública del dispositivo."""
    response = requests.get("https://api64.ipify.org?format=json")
    response.raise_for_status()
    return response.json()["ip"]

def get_geolocation(ip_address):
    """Obtiene la latitud y longitud de una dirección IP usando una API externa."""
    try:
        response = requests.get(f'https://freegeoip.app/json/{ip_address}')
        response.raise_for_status()
        data = response.json()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        if latitude is not None and longitude is not None:
            return float(latitude), float(longitude)
        else:
            return None, None
    except requests.RequestException as e:
        raise Exception(f"Error al obtener geolocalización: {e}")
