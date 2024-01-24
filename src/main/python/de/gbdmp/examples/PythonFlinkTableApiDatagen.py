from pyflink.table import *
from pyflink.table import EnvironmentSettings, TableEnvironment

# Create a TableEnvironment for batch or streaming execution
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)


# Create a source table
table_env.executeSql("""CREATE TEMPORARY TABLE SourceTable (
  f0 STRING
) WITH (
  'connector' = 'datagen',
  'rows-per-second' = '100'
)
""")

# Create a sink table
table_env.executeSql("CREATE TEMPORARY TABLE SinkTable WITH ('connector' = 'blackhole') LIKE SourceTable (EXCLUDING OPTIONS) ")

# Create a Table from a Table API query
table1 = table_env.from_path("SourceTable").select(...)

# Create a Table from a SQL query
table2 = table_env.sql_query("SELECT ... FROM SourceTable ...")

# Emit a Table API result Table to a TableSink, same for SQL result
table_result = table1.execute_insert("SinkTable")