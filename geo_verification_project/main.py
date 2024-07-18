# main.py
import os
import logging
import subprocess
from services.geo_service import get_ip_address, get_geolocation, send_geo_alert
from services.system_service import get_system_serial
from services.directory_service import get_directories_from_api, verify_directories, check_missing_directories

# Configuración de logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/app.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')


ALERT_API_URL = "https://api.gana-loterias.com/v4/geolocation"

DIRECTORIES_API_URL = "https://pocket-base-production.up.railway.app/api/collections/paths/records"


try:
    serial = get_system_serial()
    logging.info(f"Serial del sistema: {serial}")
except Exception as e:
    logging.error(f"Error al obtener el serial del sistema: {e}")
    serial = "1exc100"  


ip_address = get_ip_address()
logging.info(f"IP: {ip_address}")


latitude, longitude = get_geolocation(ip_address)
if latitude is None or longitude is None:
    logging.error("No se pudo obtener la geolocalización. Abortando envío de alertas.")
else:
    logging.info(f"Geo - Latitud: {latitude}, Longitud: {longitude}")

    # Obtener directorios desde la API
    try:
        directories = get_directories_from_api(DIRECTORIES_API_URL)
    except Exception as e:
        logging.error(f"Error al obtener directorios de la API: {e}")
        directories = []

    
    invalid_directories = verify_directories(directories)
    logging.info(f"Alerta: {invalid_directories}")

    missing_directories = check_missing_directories(directories)
    logging.info(f"Faltantes: {missing_directories}")

    if invalid_directories:
        for directory in invalid_directories:
            try:
                send_geo_alert(ALERT_API_URL, serial, f"Alerta: {directory}", float(latitude), float(longitude))
            except Exception as e:
                logging.error(e)
    else:
        try:
            send_geo_alert(ALERT_API_URL, serial, "Todos los directorios permitidos", float(latitude), float(longitude))
        except Exception as e:
            logging.error(e)

    
    if missing_directories:
        for directory in missing_directories:
            try:
                send_geo_alert(ALERT_API_URL, serial, f"Faltante: {directory}", float(latitude), float(longitude))
            except Exception as e:
                logging.error(e)
                
        try:
            subprocess.Popen([r'C:\Win_Apps\Post.lnk'], shell=True)
            logging.info("Se ejecutó el archivo Post.lnk")
        except Exception as e:
            logging.error(f"No se pudo ejecutar el archivo Post.lnk: {e}")
