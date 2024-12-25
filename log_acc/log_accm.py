from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/log', methods=['POST'])
def handle_log():
    log_message = request.json
    producer.send('logs', log_message)
    return jsonify({"status": "Log received"}), 200

@app.route('/heartbeat', methods=['POST'])
def handle_heartbeat():
    heartbeat_message = request.json
    producer.send('heartbeats', heartbeat_message)
    return jsonify({"status": "Heartbeat received"}), 200

if __name__ == "__main__":
    app.run(port=5000)
