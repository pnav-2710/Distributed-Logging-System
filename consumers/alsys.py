from flask import Flask, request, jsonify
from kafka import KafkaConsumer
import json
import threading

# Constants
LOGS_TOPIC = "logs"
KAFKA_SERVER = 'localhost:9092'
ALERT_URL = "http://localhost:5002/alert"  # Monitoring service URL to receive alerts

# Flask app for alert system
app = Flask(__name__)

# Kafka Consumer to listen for log-level WARN and ERROR messages
def consume_logs():
    consumer = KafkaConsumer(LOGS_TOPIC, bootstrap_servers=KAFKA_SERVER, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        log_entry = message.value
        if log_entry.get("log_level") in ["WARN", "ERROR"]:
            print(f"ALERT: Critical log detected: {log_entry}")

# Start the Kafka log consumer in a thread
threading.Thread(target=consume_logs, daemon=True).start()

# Flask route to handle alerts sent by monitoring.py
@app.route('/alert', methods=['POST'])
def receive_alert():
    try:
        alert_message = request.json  # Extract the JSON payload from the POST request
        if alert_message:
            # Log the received alert (node failure, for instance)
            print(f"ALERT RECEIVED: {alert_message}")
            return jsonify({"status": "success", "message": "Alert received"}), 200
        else:
            return jsonify({"status": "failure", "message": "Invalid alert format"}), 400
    except Exception as e:
        print(f"Error processing alert: {str(e)}")
        return jsonify({"status": "failure", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
