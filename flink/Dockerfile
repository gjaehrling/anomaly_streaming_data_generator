FROM flink:latest

# install python3 and pip3
RUN apt-get update -y && \
apt-get install -y python3 python3-pip python3-dev && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python

# install PyFlink
#RUN wget -P /opt/flink/ https://dlcdn.apache.org/flink/flink-1.18.1/flink-1.18.1-bin-scala_2.12.tgz

COPY apache-flink*.tar.gz /
RUN pip3 install /apache-flink-*.tar.gz && pip3 install /apache-flink*.tar.gz

mkdir /opt/flink/usrlib
COPY flink-sql-avro-1.17.1.jar /opt/flink/usrlib/
COPY flink-sql-connector-kafka-1.17.1.jar /opt/flink/usrlib/