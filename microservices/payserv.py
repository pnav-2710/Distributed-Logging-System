import requests
import time
import random
import json
import uuid
import threading
import logging

# Constants
LOG_URL = "http://localhost:5000/log"  # Endpoint for log messages
ALIVE_URL = "http://localhost:5002/alive"  # Endpoint for heartbeats
SERVICE_NAME = "payservice"  # Name of the service

# Generate a unique node ID for each instance of the script
NODE_ID = str(uuid.uuid4())

# Setup logger
logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Function to send heartbeats to the monitoring service
def send_heartbeat():
    while True:  # Keep sending heartbeats indefinitely
        heartbeat_message = {
            "node_id": NODE_ID,
            "status": "ALIVE",
            "timestamp": time.time()
        }
        try:
            # Send heartbeat to /alive endpoint
            requests.post(ALIVE_URL, json=heartbeat_message)
            logger.info(f"Heartbeat sent to {ALIVE_URL}: {heartbeat_message}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending heartbeat: {e}")
        time.sleep(5)  # Send heartbeat every 5 seconds

# Function to generate and send logs (INFO, WARN, ERROR)
def generate_logs():
    log_levels = ["INFO", "WARN", "ERROR"]
    messages = {
        "INFO": "Service is running smoothly.",
        "WARN": "Service is experiencing high latency.",
        "ERROR": "Service encountered a critical failure!"
    }

    while True:  # Keep generating logs indefinitely
        log_level = random.choice(log_levels)
        log_message = {
            "log_id": str(uuid.uuid4()),
            "node_id": NODE_ID,
            "log_level": log_level,
            "message_type": "LOG",
            "message": messages[log_level],
            "service_name": SERVICE_NAME,
            "timestamp": time.time()
        }

        # Log the message locally
        if log_level == "INFO":
            logger.info(json.dumps(log_message))
        elif log_level == "WARN":
            logger.warning(json.dumps(log_message))
        elif log_level == "ERROR":
            logger.error(json.dumps(log_message))

        # Send log message to /log endpoint
        try:
            requests.post(LOG_URL, json=log_message)
            logger.info(f"Log sent to {LOG_URL}: {log_message}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending log: {e}")

        time.sleep(10)  # Generate and send logs every 10 seconds

if __name__ == "__main__":
    # Start sending heartbeat in a separate thread
    threading.Thread(target=send_heartbeat, daemon=True).start()

    # Start generating logs in another thread
    threading.Thread(target=generate_logs, daemon=True).start()

    # Keep the main program running
    while True:
        time.sleep(1)  # Prevent the main thread from exiting

