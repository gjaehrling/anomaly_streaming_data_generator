CREATE STREAM user_data_stream
         (id STRING,
          name STRING,
          sex STRING,
          address STRING,
          city STRING,
          zip STRING,
          country STRING,
          phone STRING,
          email STRING,
          image STRING,
          date_of_birth STRING,
          profession STRING,
          created_at STRING,
          updated_at STRING,
          sourceTime BIGINT) WITH (
               KAFKA_TOPIC='sales.user_data',
               KEY_FORMAT='KAFKA',
               VALUE_FORMAT='JSON');