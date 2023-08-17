#!/usr/bin/env bash

curl -X POST -H "Content-Type: application/json" -d @../config/pinot_schema.json http://localhost:9000/schemas
