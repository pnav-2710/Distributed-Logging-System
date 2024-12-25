import uuid
import time
import logging
import json
import threading
import random
import requests

SERVICE_NAME = "PaymentService"
NODE_ID = str(uuid.uuid4())
LOG_URL = "http://localhost:5000/log"  # Log Accumulator URL
HEARTBEAT_URL = "http://localhost:5000/heartbeat"
ALERT_URL = "http://localhost:5000/alert"  # Alert System URL
HEARTBEAT_THRESHOLD = 15  # Time in seconds before considering a node as failed

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(SERVICE_NAME)

# Dictionary to store the last heartbeat timestamp for monitoring
node_status = {NODE_ID: time.time()}

def send_registration():
    registration_message = {
        "node_id": NODE_ID,
        "message_type": "REGISTRATION",
        "service_name": SERVICE_NAME,
        "timestamp": time.time()
    }
    requests.post(LOG_URL, json=registration_message)

def send_heartbeat():
    while True:
        heartbeat_message = {
            "node_id": NODE_ID,
            "message_type": "HEARTBEAT",
            "status": "UP",
            "timestamp": time.time()
        }
        requests.post(HEARTBEAT_URL, json=heartbeat_message)

        # Update node status
        node_status[NODE_ID] = time.time()

        time.sleep(5)  # Send heartbeat every 5 seconds

def monitor_nodes():
    while True:
        current_time = time.time()
        for node, last_heartbeat in list(node_status.items()):
            if current_time - last_heartbeat > HEARTBEAT_THRESHOLD:
                alert_message = {
                    "node_id": node,
                    "alert_type": "NODE_FAILURE",
                    "message": f"Node {node} has stopped sending heartbeats.",
                    "service_name": SERVICE_NAME,
                    "timestamp": current_time
                }
                logger.error(f"ALERT: {alert_message['message']}")
                requests.post(ALERT_URL, json=alert_message)

                # Remove the node from monitoring to avoid duplicate alerts
                del node_status[node]
        time.sleep(HEARTBEAT_THRESHOLD // 2)  # Check periodically

def generate_logs():
    log_levels = ["INFO", "WARN", "ERROR"]
    messages = {
        "INFO": "Service is running.",
        "WARN": "Service is experiencing high latency.",
        "ERROR": "Service encountered a critical failure!"
    }

    while True:
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

        if log_level == "INFO":
            logger.info(json.dumps(log_message))
        elif log_level == "WARN":
            logger.warning(json.dumps(log_message))
        elif log_level == "ERROR":
            logger.error(json.dumps(log_message))

        requests.post(LOG_URL, json=log_message)
        time.sleep(10)

if __name__ == "__main__":
    send_registration()
    threading.Thread(target=send_heartbeat, daemon=True).start()
    threading.Thread(target=monitor_nodes, daemon=True).start()
    generate_logs()
