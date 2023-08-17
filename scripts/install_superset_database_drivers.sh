#!/usr/bin/env bash

echo "install drivers:"

filename="../docker/requirements-local.txt"

while IFS= read -r line; do
  # Process each line
   docker exec superset_app pip install "$line"
done < "$filename"
