# Distributed Logging and Monitoring System

This project implements a distributed logging and monitoring system using Python, Flask, Kafka, and Elasticsearch. It is designed to collect logs and heartbeats from microservices, monitor their health, and provide alerting and log indexing capabilities.

## Project Structure

```
dls_finall/
├── consumers/
│   ├── alsys.py         # Alert system: receives alerts and consumes critical logs
│   └── elsearch.py      # Consumes logs from Kafka and indexes them into Elasticsearch
├── log_acc/
│   └── log_accm.py      # Log accumulator: receives logs/heartbeats and sends them to Kafka
├── microservices/
│   └── payserv.py       # Example microservice: generates logs and heartbeats
├── monitoring/
│   └── mon_serv.py      # Monitoring service: tracks node health and sends alerts
```

## Components

### 1. Microservice (`payserv.py`)
- Simulates a payment service.
- Periodically sends log messages (INFO, WARN, ERROR) and heartbeats to the system.
- Demonstrates how a real service would integrate with the logging and monitoring infrastructure.

### 2. Log Accumulator (`log_accm.py`)
- Flask app that exposes endpoints to receive logs and heartbeats from microservices.
- Forwards received data to Kafka topics (`logs`, `heartbeats`).

### 3. Monitoring Service (`mon_serv.py`)
- Flask app that receives heartbeats from nodes.
- Periodically checks for missing heartbeats to detect node failures.
- Sends alerts to the alert system if a node is considered dead.

### 4. Alert System (`alsys.py`)
- Flask app that receives alerts from the monitoring service.
- Consumes logs from Kafka and prints critical logs (WARN, ERROR).

### 5. Elasticsearch Consumer (`elsearch.py`)
- Consumes logs from Kafka and indexes them into Elasticsearch for search and analysis.

## Setup Instructions

### Prerequisites
- Python 3.7+
- [Apache Kafka](https://kafka.apache.org/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- Python packages: `flask`, `kafka-python`, `requests`, `elasticsearch`

### Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd dls_finall
   ```
2. **Install Python dependencies:**
   ```bash
   pip install flask kafka-python requests elasticsearch
   ```
3. **Start Kafka and Elasticsearch:**
   - Make sure Kafka is running on `localhost:9092` and Elasticsearch on `localhost:9200`.

### Running the System
1. **Start the Log Accumulator:**
   ```bash
   python log_acc/log_accm.py
   ```
2. **Start the Monitoring Service:**
   ```bash
   python monitoring/mon_serv.py
   ```
3. **Start the Alert System:**
   ```bash
   python consumers/alsys.py
   ```
4. **Start the Elasticsearch Consumer:**
   ```bash
   python consumers/elsearch.py
   ```
5. **Start the Example Microservice:**
   ```bash
   python microservices/payserv.py
   ```

## How It Works
- Microservices send logs and heartbeats to the log accumulator.
- The log accumulator forwards data to Kafka topics.
- The monitoring service checks for missing heartbeats and sends alerts if a node fails.
- The alert system receives alerts and prints critical logs.
- The Elasticsearch consumer indexes logs for search and analysis.

## License
MIT 