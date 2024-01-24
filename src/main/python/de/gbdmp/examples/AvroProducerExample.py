from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import json

# Define the Avro schema for your key
key_avro_schema_str = """
{
  "type": "record",
  "name": "Key",
  "fields": [
    {"name": "id", "type": "string"}
  ]
}
"""

key_avro_schema = avro.loads(key_avro_schema_str)

# Define the Avro schema for your value
value_avro_schema_str = """
{
  "type": "record",
  "name": "Sensor",
  "fields": [
    {"name": "desc", "type": "string"},
    {"name": "id", "type": "string"},
    {"name": "lat", "type": "int"},
    {"name": "lng", "type": "int"},
    {"name": "type", "type": "string"},
    {"name": "unit", "type": "string"},
    {"name": "value", "type": "float"}
  ]
}
"""

value_avro_schema = avro.loads(value_avro_schema_str)

# Create AvroProducer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://0.0.0.0:8081'
}

# Create AvroProducer instance
avro_producer = AvroProducer(conf, default_key_schema=key_avro_schema, default_value_schema=value_avro_schema)

# Your key data
key_data = {'id': 'sensor_1'}

# Your value data
value_data = {'desc': 'Main Entrance', 'id': 'Sensor_1', 'lat': 10, 'lng': 10, 'type': 'temperature', 'unit': 'C', 'value': 3.524852969230213}

# Produce Avro-serialized message to Kafka topic
avro_producer.produce(topic='your_kafka_topic', value=value_data, key=key_data)

# Ensure the message is sent to Kafka
avro_producer.flush()
