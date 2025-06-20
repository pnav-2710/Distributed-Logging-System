from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

# Initialize Elasticsearch client with 'scheme', 'host', and 'port'
es = Elasticsearch([{'scheme': 'http', 'host': 'localhost', 'port': 9200}])

# Initialize Kafka consumer for the 'logs' topic
consumer = KafkaConsumer(
    'logs', 
    bootstrap_servers='localhost:9092', 
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume messages from the Kafka topic
for message in consumer:
    log_entry = message.value
    
    # Index the log entry into Elasticsearch
    es.index(index="logs", body=log_entry)
    
    # Print the indexed log to the terminal
    print(f"Indexed log: {log_entry}")
