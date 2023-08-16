#!/usr/bin/env python3
# coding: utf-8

"""
Python Kafka Connector Class:

Maintainer Gerd Jährling mail@gerd-jaehrling.de
"""

# general imports:
import sys
from uuid import uuid4

# kafka import:
from confluent_kafka import Producer
import socket
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField, SerializationError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

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
        self.bootstrap_server = kwargs.get("bootstrap_servers", "localhost")
        self.bootstrap_server_port = kwargs.get("bootstrap_server_port", "9092")
        self.schema_registry_url = kwargs.get("schema_registry_url", "http://localhost:8081")
        self.topic = kwargs.get("topic", "test")
        self.schema = kwargs.get("schema", None)

    def send_data(self, key_value=None, data=None):
        """
        main method containing the JSON schema, connection to the schema-registry and the loop producing
        messages

        :return: none
        """

        try:
            schema_file_path = project_root + "/src/main/python/resources/schema.json"
            # Read the contents of the schema file
            with open(schema_file_path, "r") as file:
                schema_contents = file.read()
        except FileNotFoundError:
            logging.error("could not find or read file with the JSON schema!")

        try:
            logging.debug("connect to the schema registry")
            schema_registry_conf = {"url": "http://0.0.0.0:8081"}
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
        except Exception as e:
            logging.error("cannot connect to the schema registry {}".format(e))
            sys.exit(1)

        try:
            logging.debug("using string serialiser and JSON serialiser to serialise the message")
            string_serializer = StringSerializer('utf_8')
            json_serializer = JSONSerializer(str(schema_contents), schema_registry_client, self.data_to_dict)
        except SerializationError as se:
            logging.error("serialization not successful {}".format(se))

        conf = {'bootstrap.servers': "localhost:9092",
                'client.id': socket.gethostname()}
        producer = Producer(conf)

        logging.info("Producing user records to topic {}. ^C to exit.".format(self.topic))
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)

        try:
            #producer.produce(topic=self.topic, key="key", value="value")
            producer.produce(topic=self.topic,
                             key=key_value,
                             #key=string_serializer(str(uuid4())),
                             #value=json_serializer(data, SerializationContext(self.topic, MessageField.VALUE)),
                             value=data,
                             partition=4,
                             on_delivery=self.delivery_report)
        except KeyboardInterrupt:
            sys.exit(0)

        logging.info("\nFlushing records...")
        producer.flush()


    def data_to_dict(self, data, ctx):
        """
        Returns a dict representation of the data for serialization.
        Args:
            data: data instance.
            ctx (SerializationContext): Metadata pertaining to the serialization
                operation.
        Returns:
            dict: Dict populated with user attributes to be serialized.
        """

        # User._address must
        # not be serialized; omit from dict
        return data

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




