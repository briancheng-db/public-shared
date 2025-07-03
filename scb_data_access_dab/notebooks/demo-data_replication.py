# Databricks notebook source
import yaml

PRINT_MODE = True

# COMMAND ----------
# MAGIC %md
# MAGIC # Data Replication
# COMMAND ----------

# Get values from the yaml file
with open('data_replication_metadata.yaml', 'r') as file:
    data_replication_config = yaml.safe_load(file)

# COMMAND ----------
# MAGIC %md
# MAGIC # Process Data Replications
# COMMAND ----------

def create_data_replication_sql(prod_table_name, target_table_name, filter_condition=None, target_write_mode="overwrite", target_partition_column=None):
    """Create SQL for data replication based on the configuration"""

    # Base SQL template
    if target_write_mode.lower() == "overwrite":
        data_replication_sql = f"""
CREATE OR REPLACE TABLE {target_table_name}
AS
SELECT * FROM {prod_table_name}
"""
    else:
        # For append mode, we would use INSERT INTO
        data_replication_sql = f"""
INSERT INTO {target_table_name}
SELECT * FROM {prod_table_name}
"""

    # Add filter condition if specified
    if filter_condition and filter_condition is not None:
        data_replication_sql += f" WHERE {filter_condition}"

    # Add partition column if specified
    if target_partition_column and target_partition_column is not None:
        data_replication_sql += f" PARTITIONED BY ({target_partition_column})"

    return data_replication_sql

# Process all data replications
for replication in data_replication_config.get('data_replications', []):
    prod_table_name = replication['prod_table_name']
    target_table_name = replication['target_table_name']
    filter_condition = replication.get('filter_condition')
    target_write_mode = replication.get('target_write_mode', 'overwrite')
    target_partition_column = replication.get('target_partition_column')

    print(f"Processing replication: {prod_table_name} -> {target_table_name}")
    print(f"Write mode: {target_write_mode}")
    print(f"Filter condition: {filter_condition}")
    print(f"Partition column: {target_partition_column}")

    # Generate the SQL
    replication_sql = create_data_replication_sql(
        prod_table_name=prod_table_name,
        target_table_name=target_table_name,
        filter_condition=filter_condition,
        target_write_mode=target_write_mode,
        target_partition_column=target_partition_column
    )

    print("Generated SQL:")
    print(replication_sql)
    print("-" * 80)

    if not PRINT_MODE:
        spark.sql(replication_sql)

# COMMAND ----------
