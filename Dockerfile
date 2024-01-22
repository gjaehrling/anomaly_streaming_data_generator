# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/code/src/main/python"

# copy the content of the local src directory to the working directory
#COPY src/ .
COPY . .

# command to run on container start
CMD ["sh", "-c", "python ./src/main/python/de/gbdmp/anomaly_data_generator/AnomalyDataGenerator.py \
               --topic $ANOMALY_TOPIC \
               --bootstrapserver $BOOTSTRAP_SERVER --bootstrapserverport $BOOTSTRAP_SERVER_PORT \
               --schema-registry-url $SCHEMA_REGISTRY_URL \
               --num-messages $NUM_MESSAGES --contamination $CONTAMINATION" ]

#CMD [ "python3" ]