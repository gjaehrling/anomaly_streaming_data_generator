#!/usr/bin/env python3
# coding: utf-8

"""
Python Kafka Connector Class:

Maintainer Gerd Jährling mail@gerd-jaehrling.de
"""

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# import and configuration for logging
from pathlib import Path
import logging
from logging import config

# configure logging:
project_root = str(Path(__file__).parents[6])
logging_config = project_root + "/src/main/python/resources/logging.ini"
config.fileConfig(logging_config)


class PythonKafkaConnector:
    def __init__(self, **kwargs):
        self.bootstrap_server = kwargs.get("bootstrap_server", "localhost")
        self.bootstrap_server_port = kwargs.get("bootstrap_server_port", "9092")
        self.schema_registry_url = kwargs.get("schema_registry_url", "http://0.0.0.0:8081")
        self.topic = kwargs.get("topic", "iot.sensor.anomaly_data")
        self.schema = kwargs.get("schema", None)

    def send_data(self, key_value=None, data=None):
        """
        main method containing the JSON schema, connection to the schema-registry and the loop producing
        messages

        :return: none
        """

        try:
            logging.info("read the value schema from file")
            value_schema_file_path = project_root + "/src/main/python/resources/sensor_value_schema.avsc"
            # Read the contents of the schema file
            with open(value_schema_file_path, "r") as file:
                value_schema_contents = file.read()
        except FileNotFoundError:
            logging.error("could not find or read file with the JSON schema!")

        try:
            logging.info("read the key schema from file")
            value_schema_file_path = project_root + "/src/main/python/resources/sensor_key_schema.avsc"
            # Read the contents of the schema file
            with open(value_schema_file_path, "r") as file:
                key_schema_contents = file.read()
        except FileNotFoundError:
            logging.error("could not find or read file with the JSON schema!")

        try:
            logging.info("load the key schema into the schema registry")
            key_avro_schema = avro.loads(key_schema_contents)
            logging.info("load the value chema into the schema registry")
            value_avro_schema = avro.loads(value_schema_contents)
        except Exception as e:
            logging.error("could not load the schema into the schema registry: {}".format(e))

        # Create AvroProducer configuration:
        # for local testing parameters needs to be set to:
        #    'bootstrap.servers': 'localhost:9092',
        #    'schema.registry.url': 'http://0.0.0.0:8081'

        conf = {
            'bootstrap.servers': self.bootstrap_server + ":" + self.bootstrap_server_port,
            'schema.registry.url': self.schema_registry_url
        }

        # Create AvroProducer instance
        avro_producer = AvroProducer(conf,
                                     default_key_schema=key_avro_schema,
                                     default_value_schema=value_avro_schema)

        # Produce Avro-serialized message to Kafka topic
        avro_producer.produce(topic=self.topic, value=data, key=key_value)

        # Ensure the message is sent to Kafka
        avro_producer.flush()

    def delivery_report(self, err, msg):
        """
        Reports the success or failure of a message delivery.
        Args:
            err (KafkaError): The error that occurred on None on success.
            msg (Message): The message that was produced or failed.
        """

        if err is not None:
            logging.error("Delivery failed for User record {}: {}".format(msg.key(), err))
            return
        logging.info('User record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))



