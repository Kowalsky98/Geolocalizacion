# services/geo_service.py
import requests

def get_ip_address():
    response = requests.get("https://api64.ipify.org?format=json")
    return response.json()["ip"]

def get_geolocation(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
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

def send_geo_alert(api_url, serial, alert_type, latitude, longitude):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "serial": serial,
        "alert": True,
        "alertType": alert_type,
        "latitude": float(latitude),
        "longitude": float(longitude)
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Error al enviar la alerta: {response.status_code} - {response.text}")
