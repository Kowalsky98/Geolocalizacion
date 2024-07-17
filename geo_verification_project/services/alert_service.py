# services/alert_service.py
import requests

def generate_alert(serial, latitude, longitude, alert, alert_type):
    data = {
        "serial": serial,
        "alert": alert,
        "alertType": alert_type,
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.post("https://api.gana-loterias.com/v4/geolocation", json=data)
    return response.status_code
