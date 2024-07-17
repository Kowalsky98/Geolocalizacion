# main.py
import time
import logging
import os
from services.geo_service import get_geolocation, get_ip
from services.directory_service import verify_directories
from services.alert_service import generate_alert
from services.system_info import get_system_serial
from config.config import DIRECTORIES_TO_CHECK

# Crear el directorio de logs si no existe
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuración del log
logging.basicConfig(filename='logs/app.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def main():
    try:
        # Obtener la IP del equipo
        ip_address = get_ip()
        
        # Obtener la geolocalización basada en la IP
        latitude, longitude = get_geolocation(ip_address)
        
        # Obtener el serial del equipo
        serial = get_system_serial()
        
        # Verificar la existencia de los directorios especificados
        missing_directories = verify_directories(DIRECTORIES_TO_CHECK)
        
        # Determinar el tipo de alerta basado en los directorios encontrados
        if missing_directories:
            alert_type = "system not found"
            alert = True
        else:
            alert_type = "another system found"
            alert = False
        
        # Generar y enviar la alerta
        response_status = generate_alert(serial, latitude, longitude, alert, alert_type)
        if response_status == 202:
            logging.info("Alerta enviada correctamente.")
        else:
            logging.error("Error al enviar la alerta.")
    except Exception as e:
        logging.error(f"Error en el proceso principal: {e}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(3600)  # Ejecutar cada hora
