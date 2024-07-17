# services/directory_service.py
import os

def verify_directories(directories):
    missing_directories = [dir for dir in directories if not os.path.exists(dir)]
    return missing_directories
