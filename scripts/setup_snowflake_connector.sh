#!/usr/bin/env bash

curl -X POST -H "Content-Type: application/json" --data @../config/SnowflakeSinkConnectorConnector_config.json http://localhost:8083/connectors