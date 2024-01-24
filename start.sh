#!/usr/bin/env bash

# Start the first process
echo "Choose an option for containers to be started (confluent/postgres/airflow/spark/superset/flink/datagen/notebook/all): "
read option

case "$option" in
    confluent) docker-compose up -d zookeeper broker schema-registry connect rest-proxy ksqldb-server ksqldb-cli rest-proxy control-center;;
    postgres) docker-compose up -d postgres_primary postgres_replica;;
    datagen) docker-compose up -d streaming_data_generator;;
    spark) docker-compose up -d spark-master spark-worker-1 spark-worker-2;;
    airflow) docker-compose up -d postgres redis airflow-webserver airflow-scheduler airflow-worker airflow-triggerer airflow-init airflow-cli flower;;
    notebook) docker-compose up jupyter;;
    flink) docker-compose up -d jobmanager taskmanager;;
    superset) docker-compose up -d superset;;
    all) docker-compose up -d;;
    *) echo "Unknown option";;
esac