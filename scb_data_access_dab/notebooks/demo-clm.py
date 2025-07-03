# Databricks notebook source

# import the necessary libraries, e.g. yaml parser, etc.
import yaml

PRINT_MODE = False

# COMMAND ----------
# MAGIC %md
# MAGIC # 1. Load configuration from YAML
# COMMAND ----------

# Get values from the yaml file
with open('clm_metadata.yaml', 'r') as file:
    clm_config = yaml.safe_load(file)

# COMMAND ----------
# MAGIC %md
# MAGIC # 2. Create masking functions
# COMMAND ----------

def create_masking_function(func_name, mask_value, grant_groups):
    """Create a masking function with the specified parameters"""

    # Create grant group conditions
    clm_grant_group_condition_template = "is_account_group_member('{group_name}')"
    clm_grant_group_conditions = [clm_grant_group_condition_template.format(group_name=group_name) for group_name in grant_groups]
    clm_grant_group_conditions_str = " OR ".join(clm_grant_group_conditions)

    # Create the function SQL
    clm_func_sql = f"""
CREATE OR REPLACE FUNCTION {func_name}(column_value STRING)
RETURN
  IF({clm_grant_group_conditions_str}, column_value, '{mask_value}');
"""

    print(f"Creating function: {func_name}")
    print(clm_func_sql)

    if not PRINT_MODE:
        spark.sql(clm_func_sql)

    return clm_func_sql


# COMMAND ----------
# MAGIC %md
# MAGIC # 3. Grant EXECUTE privileges to groups
# COMMAND ----------

def grant_function_privileges(func_name, grant_groups):
    """Grant EXECUTE privileges on function to specified groups"""

    clm_grant_sql_template = """
                              GRANT EXECUTE ON FUNCTION {func_name} TO `{group_name}`;
                              """

    for group_name in grant_groups:
        clm_grant_sql = clm_grant_sql_template.format(func_name=func_name, group_name=group_name)
        print(f"Granting privileges on {func_name} to {group_name}")
        print(clm_grant_sql)
        if not PRINT_MODE:
            spark.sql(clm_grant_sql)


# COMMAND ----------
# MAGIC %md
# MAGIC # 4. Apply masking functions to tables
# COMMAND ----------

def apply_masking_to_table(table_name, masking_configs):
    """Apply masking functions to specified columns in a table"""

    for masking_config in masking_configs:
        masking_function = masking_config['masking_function']
        columns = masking_config['columns']

        for column in columns:
            pii_clm_table_sql = f"""
                                ALTER TABLE
                                  {table_name}
                                ALTER COLUMN
                                  {column}
                                SET
                                  MASK {masking_function};
                                """
            print(f"Applying {masking_function} to {table_name}.{column}")
            print(pii_clm_table_sql)
            if not PRINT_MODE:
                spark.sql(pii_clm_table_sql)


# COMMAND ----------

if __name__ == "__main__":
  # Create all masking functions
  for masking_func in clm_config.get('masking_functions', []):
      func_name = masking_func['name']
      mask_value = masking_func['mask_value']
      grant_groups = masking_func['pii_grant_groups']

      create_masking_function(func_name, mask_value, grant_groups)

  # Grant privileges for all masking functions
  for masking_func in clm_config.get('masking_functions', []):
      func_name = masking_func['name']
      grant_groups = masking_func['exec_grant_groups']

      grant_function_privileges(func_name, grant_groups)

  # Apply masking to all tables
  for table_config in clm_config.get('table_apply', []):
      table_name = table_config['table_name']
      apply_mask_configs = table_config['apply_mask']

      apply_masking_to_table(table_name, apply_mask_configs)

# COMMAND ----------
# MAGIC %md
# MAGIC # 5. Test the masking functions
# COMMAND ----------

# Test all masking functions
for masking_func in clm_config.get('masking_functions', []):
    func_name = masking_func['name']
    mask_value = masking_func['mask_value']

    clm_test_sql = f"""
                    SELECT {func_name}('test') as masked_value
                    """
    print(f"Testing function: {func_name}")
    print(clm_test_sql)

    if not PRINT_MODE:
        spark.sql(clm_test_sql)