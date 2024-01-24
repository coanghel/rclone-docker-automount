import requests
import os
import time
import json
import logging
from requests.auth import HTTPBasicAuth

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Environment variables
USERNAME = os.getenv('RCLONE_USERNAME')
PASSWORD = os.getenv('RCLONE_PASSWORD')
PORT = os.getenv('RCLONE_PORT') or '5572'
# Constants
RCLONE_URL = f"http://rclone:{PORT}"
AUTH = HTTPBasicAuth(USERNAME, PASSWORD) if USERNAME and PASSWORD else None
HEADERS = {'Content-Type': 'application/json', 'User-Agent': 'RcloneClient/1.0'}
RETRY_INTERVAL = 10  # seconds

def is_rclone_ready():
    try:
        response = requests.options(f"{RCLONE_URL}/rc/noopauth", auth=AUTH)
        return response.ok
    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking rclone readiness: {e}")
        return False

def read_mount_payloads():
    try:
        with open('mounts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("mounts.json file not found.")
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from the mounts.json file.")
    return None

def mount_payloads(mount_payloads):
    all_mount_success = True
    for mount_payload in mount_payloads:
        try:
            logging.info(f"Mounting {mount_payload['fs']} to {mount_payload['mountPoint']}")
            response = requests.post(f"{RCLONE_URL}/mount/mount", json=mount_payload, headers=HEADERS, auth=AUTH)
            if response.ok:
                logging.info(f"Mount successful.")
            else:
                logging.error(f"Failed to mount {mount_payload['fs']}: Status code: {response.status_code}, Response: {response.text}")
                all_mount_success = False
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            all_mount_success = False
    return all_mount_success

def initialize():
    logging.info("Waiting for rclone service to be available...")
    while not is_rclone_ready():
        logging.info(f"Rclone not ready, waiting {RETRY_INTERVAL} seconds...")
        time.sleep(RETRY_INTERVAL)
    logging.info("Rclone is ready.")

    mount_payloads_data = read_mount_payloads()
    if mount_payloads_data is None:
        return False   
    return mount_payloads(mount_payloads_data)

if __name__ == '__main__':
    if initialize():
        logging.info("Rclone initialization complete.")
    else:
        logging.error("Rclone initialization failed.")