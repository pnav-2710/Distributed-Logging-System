import time
import logging
import requests
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Configuration
ALIVE_THRESHOLD = 10  # Threshold in seconds for detecting node failure (no "alive" message)
ALERT_URL = "http://localhost:5001/alert"  # Alert system URL

# Data Structures
node_status = {}  # Stores the last timestamp when each node was marked as alive
failed_nodes = set()  # Tracks nodes that have been marked as failed

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("MonitoringService")

@app.route('/alive', methods=['POST'])
def receive_alive_message():
    """Receive the 'alive' message from each node."""
    alive_message = request.json
    node_id = alive_message.get("node_id")
    timestamp = alive_message.get("timestamp")

    if node_id:
        node_status[node_id] = timestamp
        logger.info(f"Received alive message from node {node_id}")
        print(f"Node {node_id} is ALIVE. Timestamp updated.")

        # If the node is in the failed list but comes back online, reset its failure status
        if node_id in failed_nodes:
            failed_nodes.remove(node_id)
            logger.info(f"Node {node_id} is back online.")
            print(f"Node {node_id} is BACK ONLINE.")
        
        return jsonify({"status": "success", "message": "Alive message received"}), 200
    else:
        return jsonify({"status": "failure", "message": "Invalid alive message"}), 400

def monitor_nodes():
    """Periodically check for nodes that have stopped sending 'alive' messages."""
    while True:
        current_time = time.time()

        for node_id, last_alive_time in list(node_status.items()):
            # Check the difference in time since the last "alive" message was received
            time_diff = current_time - last_alive_time

            if time_diff <= ALIVE_THRESHOLD:
                logger.info(f"Node {node_id} is alive. Last heartbeat was {time_diff:.2f} seconds ago.")
                print(f"Node {node_id} is ALIVE. Last heartbeat {time_diff:.2f} seconds ago.")
            else:
                # If the difference exceeds the threshold, consider the node dead
                if node_id not in failed_nodes:
                    logger.error(f"Node {node_id} failed. It has not sent an alive message in the last {ALIVE_THRESHOLD} seconds.")
                    print(f"Node {node_id} is DEAD. No heartbeat for {time_diff:.2f} seconds.")

                    # Send an alert (if you have an alert system)
                    alert_message = {
                        "node_id": node_id,
                        "alert_type": "NODE_FAILURE",
                        "message": f"Node {node_id} has not sent an alive message in over {ALIVE_THRESHOLD} seconds.",
                        "timestamp": current_time
                    }

                    try:
                        requests.post(ALERT_URL, json=alert_message)
                    except Exception as e:
                        logger.error(f"Failed to send alert: {str(e)}")
                        print(f"Failed to send alert for Node {node_id}: {str(e)}")

                    failed_nodes.add(node_id)

        # Sleep for a short time before checking again
        time.sleep(ALIVE_THRESHOLD // 2)

if __name__ == "__main__":
    # Start the monitoring thread
    threading.Thread(target=monitor_nodes, daemon=True).start()
    # Start the Flask app to listen for "alive" messages
    app.run(host="0.0.0.0", port=5002, debug=False)


