import os

ALERT_API_URL = "https://api.gana-loterias.com/v4/geolocation"
DIRECTORIES_API_URL = "https://pocket-base-production.up.railway.app/api/collections/paths/records"

POST_FILE_PATH = r"C:\Win_Apps\Post.lnk"

LOG_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'GeoVerificationProject', 'logs')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'app.log')
