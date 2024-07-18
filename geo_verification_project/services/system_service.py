
import subprocess

def get_system_serial():
    try:
        result = subprocess.check_output('wmic bios get serialnumber', shell=True)
        serial = result.decode().split('\n')[1].strip()
        return serial
    except Exception as e:
        raise Exception(f"Error al obtener el serial del sistema: {e}")
