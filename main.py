import os
import logging
from services.geo_service import get_ip_address, get_geolocation
from services.system_service import get_system_serial
from services.directory_service import get_directories_from_api, verify_directories, check_missing_directories
from services.alert_service import send_geo_alert  
from config.config import ALERT_API_URL, DIRECTORIES_API_URL, POST_FILE_PATH

if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

try:
    serial = get_system_serial()
    logging.info(f"Serial del sistema: {serial}")
except Exception as e:
    logging.error(f"Error al obtener el serial del sistema: {e}")
    serial = "1exc100"  # Valor predeterminado en caso de fallo

ip_address = get_ip_address()
logging.info(f"IP: {ip_address}")

latitude, longitude = get_geolocation(ip_address)
if latitude is None or longitude is None:
    logging.error("No se pudo obtener la geolocalización. Abortando envío de alertas.")
else:
    logging.info(f"Geo - Latitud: {latitude}, Longitud: {longitude}")
    try:
        directories = get_directories_from_api(DIRECTORIES_API_URL)
    except Exception as e:
        logging.error(f"Error al obtener directorios de la API: {e}")
        directories = []

    invalid_directories = verify_directories(directories)
    missing_directories = check_missing_directories(directories)

    if invalid_directories:
        for directory in invalid_directories:
            send_geo_alert(ALERT_API_URL, serial, f"Alerta: {directory}", float(latitude), float(longitude), True)
            logging.info(f"Alerta enviada para directorio no permitido: {directory}")
    if missing_directories:
        send_geo_alert(ALERT_API_URL, serial, "Faltan directorios Ejecutando Post.lnk", float(latitude), float(longitude), False)
        logging.info("Alerta enviada. Ejecutando Post.lnk")
        os.startfile(POST_FILE_PATH) 
    if not missing_directories and not invalid_directories:
        send_geo_alert(ALERT_API_URL, serial, "Equipo funcionando correctamente", float(latitude), float(longitude), False)
        logging.info("Todos los directorios son correctos. Alerta enviada.")
