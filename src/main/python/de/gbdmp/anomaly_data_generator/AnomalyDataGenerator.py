#!/usr/bin/env python3
"""
Python Anomaly Streaming Data Generator:
Generate random IoT example data with anomalies

Maintainer Gerd Jährling mail@gerd-jaehrling.de
"""

# general imports
import sys
import json
import time
import random
from pathlib import Path
from uuid import uuid4

from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField, SerializationError

# local imports:
from de.gbdmp.anomaly_data_generator import PythonKafkaConnector

# imports for anomaly generation:
from pyod.utils.data import generate_data
from pyod.models.knn import KNN
import numpy as np

# for logging
import logging
from logging import config

# configure logging:
project_root = str(Path(__file__).parents[6])
logging_config = project_root + "/src/main/python/resources/logging.ini"
config.fileConfig(logging_config)


def generate_fake_data(**kwargs):
    """
    generate fake data for the sensors for all sensors in the config file

    :param kwargs:
    :return:
    """

    for sensor in sensors.keys():
        # generate data for each sensor:

        if sensors[sensor]["anomaly"] == "false":
            logging.debug("anomaly for sensor {} is false setting contamination to zero".format(sensor))
            contamination = 0.00
        else:
            logging.debug("anomaly for sensor {} is true setting contamination to 0.05".format(sensor))
            contamination = kwargs.get("contamination", 1)

        # generate fake data with anomalies using pyod:
        try:
            X, y = generate_data(n_train=kwargs.get("number"), contamination=contamination, n_features=1, train_only=True, random_state=1)
        except Exception as e:
            logging.error("cannot generate data for sensor {} {}".format(sensor, e))
            continue

        logging.info("X: {}".format(X))
        permutation_indices = np.random.permutation(len(X))
        X = X[permutation_indices]
        y = y[permutation_indices]

        # store the data in the sensors dict.
        # As generate_data returns a list of lists, we need to flatten it and convert to a list.
        sensors[sensor]["values"] = X.flatten().tolist()

    return sensors


def send_messages(**kwargs):
    """
    send the data to the kafka broker
    """

    #keys = list(kwargs.get(sensors.keys()))
    global generated_data
    num_messages = kwargs.get("number")

    try:
        logging.info("get the generated fake data including anomaly values. To send to Kafka")
        generated_data = kwargs.get("data")
    except Exception as e:
        logging.error("error in generating data {}".format(e))

    # initialise the kafka producer:
    connector = PythonKafkaConnector.PythonKafkaConnector(topic=topic)
    string_serializer = StringSerializer('utf_8')

    # send the data to the kafka broker:
    for i in range(num_messages):
        for d in generated_data.keys():
            delay = random.uniform(0, 2)
            #print("key: " + d, " values: " + str(generated_data[d]), " single value: " + str(generated_data[d]["values"][i]))

            key = d

            data = {
                "lat": generated_data[d]["lat"],
                "lng": generated_data[d]["lng"],
                "unit": generated_data[d]["unit"],
                "type": generated_data[d]["type"],
                "desc": generated_data[d]["desc"],
                "value": generated_data[d]["values"][i]
            }

            payload = json.dumps(data)

            logging.info("payload: {}".format(payload))
            connector.send_data(key, payload)

            time.sleep(delay)


def run(topic, bootstrap_server, bootstrap_server_port, schema_registry, schema_registry_port):
    """
    main method containing the JSON schema, connection to the schema-registry and the loop producing
    messages

    :return: none
    """
    pass


if __name__ == '__main__':
    """
    main method using a parameter to the topic:
    """

    # define the parameters:
    """
    parser = argparse.ArgumentParser("define the topic")
    parser.add_argument("--topic", help="define the name of the topic", required=True)
    parser.add_argument("--bootstrapserver", help="hostname or address of the kafka broker", required=True)
    parser.add_argument("--bootstrapserverport", help="port the kafka broker", required=True)
    parser.add_argument("--schemaregistry", help="hostname or address of the schema registry", required=True)
    parser.add_argument("--schemaregistryport", help="port for schema registry", required=True)
    parser.add_argument("--num-messages", help="number of messages -1 for infinite", default=1000, required=True)

    args = parser.parse_args()
    """
    # read config file:
    project_root = str(Path(__file__).parents[6])
    config_path = project_root + "/" + "/src/main/python/resources/config.json"

    try:
        with open(config_path) as handle:
            config = json.load(handle)
            misc_config = config.get("misc", {})
            sensors = config.get("sensors")

            interval_ms = misc_config.get("interval_ms", 500)
            verbose = misc_config.get("verbose", False)

            if not sensors:
                logging.warning("no sensors specified in config, nothing to do")
                pass

            # ToDo: call the fuction with kwargs
            topic = "iot.sensor.anomaly_data"

            data = generate_fake_data(number=100, sensors=sensors, contamination=0.1, n_features=1, train_only=True, random_state=1)
            send_messages(number=5, data=data)

    except IOError as error:
        logging.error("Error opening config file {} {}".format(config_path, error))


    try:
        pass
        #logging.info("call run method with parameters: ".format(args))
        #run(args.topic, args.bootstrapserver, args.bootstrapserverport, args.schemaregistry, args.schemaregistryport)
    except Exception as e:
        logging.error("cannot call run method".format(e))
        sys.exit(1)

