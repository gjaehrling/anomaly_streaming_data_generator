################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
import logging
from logging import config
import sys
from pathlib import Path
import requests

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaProducer, FlinkKafkaConsumer
from pyflink.datastream.formats.avro import AvroRowSerializationSchema, AvroRowDeserializationSchema

# configure logging:
project_root = str(Path(__file__).parents[6])
logging_config = project_root + "/src/main/python/resources/logging.ini"
config.fileConfig(logging_config)

def read_the_schema_from_schema_registry(topic):
    topic = "'sensors.anomalies-value'"

    SCHEMA_REGISTRY_URL = "http://schema-registry:8081"
    print("SCHEMA_REGISTRY_URL: ", SCHEMA_REGISTRY_URL)
    URL = SCHEMA_REGISTRY_URL + '/subjects/' + topic + '/versions/latest/schema'
    response = requests.get(url=URL)
    schema_data = response.json()
    avro_schema = schema_data

    return avro_schema


# Make sure that the Kafka cluster is started and the topic 'test_avro_topic' is
# created before executing this job.
def write_to_kafka(env):
    ds = env.from_collection([
        (1, 'hi'), (2, 'hello'), (3, 'hi'), (4, 'hello'), (5, 'hi'), (6, 'hello'), (6, 'hello')],
        type_info=Types.ROW([Types.INT(), Types.STRING()]))

    serialization_schema = AvroRowSerializationSchema(
        avro_schema_string="""
            {
                "type": "record",
                "name": "TestRecord",
                "fields": [
                    {"name": "id", "type": "int"},
                    {"name": "name", "type": "string"}
                ]
            }"""
    )

    kafka_producer = FlinkKafkaProducer(
        topic='test_avro_topic',
        serialization_schema=serialization_schema,
        producer_config={'bootstrap.servers': 'broker:29092', 'group.id': 'test_group'}
    )

    # note that the output type of ds must be RowTypeInfo
    ds.add_sink(kafka_producer)
    env.execute()


def read_from_kafka(env):
    """
    main method containing the JSON schema, connection to the schema-registry and the loop producing
    :param env:
    :return:
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


    deserialization_schema = AvroRowDeserializationSchema(
        avro_schema_string=value_schema_contents
    )

    kafka_consumer = FlinkKafkaConsumer(
        topics='sensors.anomalies',
        deserialization_schema=deserialization_schema,
        properties={'bootstrap.servers': 'broker:29092', 'group.id': 'test_group_1'}
    )
    kafka_consumer.set_start_from_earliest()
    ds = env.add_source(kafka_consumer)
    ds.print()
    #env.add_source(kafka_consumer).print()
    env.execute('kafka_datastream_api')


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars("file:///opt/flink/usrlib/flink-sql-avro-1.17.1.jar",
                 "file:///opt/flink/usrlib/flink-sql-connector-kafka-1.17.1.jar")

    #print("start writing data to kafka")
    #write_to_kafka(env)

    print("start reading data from kafka")
    read_from_kafka(env)