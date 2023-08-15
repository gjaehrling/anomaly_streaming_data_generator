# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
#COPY src/ .
COPY . .

# command to run on container start
CMD [ "python", "./src/main/python/de/gbdmp/streaming_data_generator/Generator.py", \
        "--topic", "sales.user_data", \
        "--bootstrapserver", "broker", "--bootstrapserverport", "29092", \
        "--schemaregistry", "schema-registry", "--schemaregistryport", "8081"]
#CMD [ "python3" ]