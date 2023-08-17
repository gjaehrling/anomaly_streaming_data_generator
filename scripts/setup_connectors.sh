#!/usr/bin/env bash

echo "initialise clickstram connector: "
curl -i -X PUT -H "Content-Type:application/json" \
    http://localhost:8083/connectors/weblogs-clickstreams/config \
    -d '{
        "connector.class"          : "io.confluent.kafka.connect.datagen.DatagenConnector",
        "kafka.topic"              : "clickstream",
        "quickstart"               : "clickstream",
        "output.data.format"       : "json",
        "format"                   : "json",
        "maxInterval"              : "30",
        "value.converter.class"    : "org.apache.kafka.connect.json.JsonConverter"
      }'

