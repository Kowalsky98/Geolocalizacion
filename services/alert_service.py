# services/alert_service.py
import requests

def send_geo_alert(api_url, serial, alert_type, latitude, longitude, alert_status):
    """Envía una alerta geolocalizada a una API externa, incluyendo el estado de la alerta."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "serial": serial,
        "alert": alert_status,
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
