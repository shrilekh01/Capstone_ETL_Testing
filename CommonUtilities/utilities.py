import os.path

import pandas as pd
import pytest
from sqlalchemy import create_engine
import oracledb
import paramiko

from Configuration.etlconfig import *
import logging

# Logging configution
logging.basicConfig(
    filename="Logs/etljob.log",
    filemode="w",
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def sales_data_from_Linux_server(self):
    # download the sales frile form Linux server to local via SFTP/ssh
    try:
        logger.info("Sales file from Linux server doenload started...")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(hostname, username=username, password=password)
        sftp = ssh_client.open_sftp()
        sftp.get(remote_file_path, local_file_path)
        sftp.close()
        ssh_client.close()
        logger.info("Sales file from Linux server doenload completed...")
    except Exception as e:
        logger.error("Error while donloading the sales file from Linux server.")


def verify_expected_as_file_to_actual_as_database(file_path, file_type, db_engine, table_name, test_case_name):
    try:
        if file_type == 'csv':
            df_expected = pd.read_csv(file_path)
        elif file_type == 'json':
            df_expected = pd.read_json(file_path)
        elif file_type == 'xml':
            df_expected = pd.read_xml(file_path, xpath=".//item")
        else:
            raise ValueError(f"unsupported file type passed{file_path}")
        logger.info(f"Expected data in the file is {df_expected}")
        query_actual = f"select * from {table_name}"
        df_actual = pd.read_sql(query_actual, db_engine)
        logger.info(f"Actual data in the file is {df_actual}")

        # expected minus atcual data (  extra data in expected )
        df_extra = df_expected[~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]
        df_extra.to_csv(f"Differences/extra_rows_in_expected_{test_case_name}.csv", index=False)

        # actual data minus expected (  extra data in actual )
        df_missing = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]
        df_missing.to_csv(f"Differences/extra_rows_in_actual_{test_case_name}.csv", index=False)

        assert df_extra.empty, (
            f"{test_case_name} : extra rows found in {df_extra} \n"
            f"check Differences/extra_rows_in_expected{test_case_name}.csv"
        )

        assert df_missing.empty, (
            f"{test_case_name} : extra rows found in {df_missing} \n"
            f"check Differences/extra_rows_in_actual_{test_case_name}.csv"
        )
    except Exception as e:
        logger.error(f"there is exception raised while check{e}")
        pytest.fail()


def verify_expected_as_database_to_actual_as_database(db_engine_expected, query_expected, db_engine_actual,
                                                      query_actual):
    df_expected = pd.read_sql(query_expected, db_engine_expected)
    logger.info(f"Expected data in the file is {df_expected}")
    df_actual = pd.read_sql(query_actual, db_engine_actual)
    logger.info(f"Actual data in the file is {df_actual}")

    assert df_actual.equals(
        df_expected), f"expeected data in {query_expected} does not match with actual data in {query_actual}"


def check_for_duplicates_across_all_the_columns(file_path, file_type):
    try:
        if file_type == 'csv':
            df_data = pd.read_csv(file_path)
        elif file_type == 'json':
            df_data = pd.read_json(file_path)
        elif file_type == 'xml':
            df_data = pd.read_xml(file_path, xpath=".//item")
        else:
            raise ValueError(f"unsupported file type passed{file_path}")
        # logger.info(f"data in the file is {df_data}")

        if df_data.duplicated().any():
            return False
        else:
            return True
    except Exception as e:
        logger.error(f"Error while reading the file {file_path}")


def check_for_duplicates_for_specific_columns(file_path, file_type, column_names):
    """
    Check for duplicates in specific columns of a file

    Args:
        file_path: Path to the file
        file_type: Type of file ('csv', 'json', 'xml')
        column_names: List of column names to check for duplicates

    Returns:
        True if no duplicates found, False if duplicates exist
    """
    try:
        # Read file based on type
        if file_type == 'csv':
            df_data = pd.read_csv(file_path)
        elif file_type == 'json':
            df_data = pd.read_json(file_path)
        elif file_type == 'xml':
            df_data = pd.read_xml(file_path, xpath=".//item")
        else:
            raise ValueError(f"Unsupported file type passed: {file_path}")

        logger.info(f"Checking duplicates for columns {column_names} in file {file_path}")

        # Check if specified columns exist in dataframe
        missing_cols = [col for col in column_names if col not in df_data.columns]
        if missing_cols:
            logger.error(f"Columns {missing_cols} not found in {file_path}")
            raise ValueError(f"Columns {missing_cols} not found in file")

        # Check for duplicates in specific columns
        if df_data.duplicated(subset=column_names).any():
            duplicate_rows = df_data[df_data.duplicated(subset=column_names, keep=False)]
            logger.warning(f"Duplicates found in columns {column_names}: \n{duplicate_rows}")
            return False
        else:
            logger.info(f"No duplicates found in columns {column_names}")
            return True

    except Exception as e:
        logger.error(f"Error while checking duplicates in file {file_path}: {e}")
        raise


def check_for_duplicates_for_database_table(db_engine, table_name, column_names=None):
    """
    Check for duplicates in database table

    Args:
        db_engine: Database connection engine
        table_name: Name of the table to check
        column_names: List of column names to check (optional). If None, checks all columns

    Returns:
        True if no duplicates found, False if duplicates exist
    """
    try:
        # Read table data
        query = f"SELECT * FROM {table_name}"
        df_data = pd.read_sql(query, db_engine)

        logger.info(f"Checking duplicates in table {table_name}")

        # Check for duplicates
        if column_names:
            # Check if specified columns exist
            missing_cols = [col for col in column_names if col not in df_data.columns]
            if missing_cols:
                logger.error(f"Columns {missing_cols} not found in table {table_name}")
                raise ValueError(f"Columns {missing_cols} not found in table")

            # Check duplicates in specific columns
            if df_data.duplicated(subset=column_names).any():
                duplicate_rows = df_data[df_data.duplicated(subset=column_names, keep=False)]
                logger.warning(f"Duplicates found in table {table_name} for columns {column_names}: \n{duplicate_rows}")
                return False
            else:
                logger.info(f"No duplicates found in table {table_name} for columns {column_names}")
                return True
        else:
            # Check duplicates across all columns
            if df_data.duplicated().any():
                duplicate_rows = df_data[df_data.duplicated(keep=False)]
                logger.warning(f"Duplicates found in table {table_name}: \n{duplicate_rows}")
                return False
            else:
                logger.info(f"No duplicates found in table {table_name}")
                return True

    except Exception as e:
        logger.error(f"Error while checking duplicates in table {table_name}: {e}")
        raise


def check_for_null_values(file_path, file_type):
    try:
        if file_type == 'csv':
            df_data = pd.read_csv(file_path)
        elif file_type == 'json':
            df_data = pd.read_json(file_path)
        elif file_type == 'xml':
            df_data = pd.read_xml(file_path, xpath=".//item")
        else:
            raise ValueError(f"unsupported file type passed{file_path}")
        # logger.info(f"data in the file is {df_data}")

        if df_data.isnull().values.any():
            return False
        else:
            return True
    except Exception as e:
        logger.error(f"Error while reading the file {file_path}")


def check_for_null_values_in_database_table(db_engine, table_name, column_names=None):
    """
    Check for null values in database table

    Args:
        db_engine: Database connection engine
        table_name: Name of the table to check
        column_names: List of column names to check (optional). If None, checks all columns

    Returns:
        True if no null values found, False if null values exist
    """
    try:
        # Read table data
        query = f"SELECT * FROM {table_name}"
        df_data = pd.read_sql(query, db_engine)

        logger.info(f"Checking null values in table {table_name}")

        if column_names:
            # Check if specified columns exist
            missing_cols = [col for col in column_names if col not in df_data.columns]
            if missing_cols:
                logger.error(f"Columns {missing_cols} not found in table {table_name}")
                raise ValueError(f"Columns {missing_cols} not found in table")

            # Check null values in specific columns
            if df_data[column_names].isnull().values.any():
                null_summary = df_data[column_names].isnull().sum()
                logger.warning(f"Null values found in table {table_name}: \n{null_summary[null_summary > 0]}")
                return False
            else:
                logger.info(f"No null values found in table {table_name} for specified columns")
                return True
        else:
            # Check null values across all columns
            if df_data.isnull().values.any():
                null_summary = df_data.isnull().sum()
                logger.warning(f"Null values found in table {table_name}: \n{null_summary[null_summary > 0]}")
                return False
            else:
                logger.info(f"No null values found in table {table_name}")
                return True

    except Exception as e:
        logger.error(f"Error while checking null values in table {table_name}: {e}")
        raise


def check_file_existence(file_path):
    try:
        if os.path.isfile(file_path):
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"file :{file_path} does not exist {e}")


def check_file_size(file_path):
    try:
        if os.path.getsize(file_path) != 0:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"file :{file_path} is zero byte file {e}")


def check_referential_integrity(db_engine, parent_table, parent_column, child_table, child_column):
    """
    Check referential integrity between parent and child tables

    Args:
        db_engine: Database connection engine
        parent_table: Name of parent table (referenced table)
        parent_column: Column name in parent table (primary key)
        child_table: Name of child table (referencing table)
        child_column: Column name in child table (foreign key)

    Returns:
        True if referential integrity is maintained, False otherwise
    """
    try:
        logger.info(f"Checking referential integrity: {child_table}.{child_column} -> {parent_table}.{parent_column}")

        # Query to find orphan records (child records without parent)
        query = f"""
        SELECT DISTINCT c.{child_column}
        FROM {child_table} c
        LEFT JOIN {parent_table} p ON c.{child_column} = p.{parent_column}
        WHERE p.{parent_column} IS NULL AND c.{child_column} IS NOT NULL
        """

        df_orphans = pd.read_sql(query, db_engine)

        if not df_orphans.empty:
            logger.error(
                f"Referential integrity violation found: {len(df_orphans)} orphan records in {child_table}.{child_column}")
            logger.error(f"Orphan values: \n{df_orphans}")
            return False
        else:
            logger.info(
                f"Referential integrity maintained: {child_table}.{child_column} -> {parent_table}.{parent_column}")
            return True

    except Exception as e:
        logger.error(f"Error while checking referential integrity: {e}")
        raise


def check_data_type_schema(db_engine, table_name, expected_schema):
    """
    Check if table schema matches expected data types

    Args:
        db_engine: Database connection engine
        table_name: Name of the table to check
        expected_schema: Dictionary with column names as keys and expected data types as values
                        Example: {'product_id': 'int64', 'product_name': 'object', 'price': 'float64'}

    Returns:
        True if schema matches, False otherwise
    """
    try:
        logger.info(f"Checking schema for table {table_name}")

        # Read table data (just first row to get schema)
        query = f"SELECT * FROM {table_name} LIMIT 1"
        df_data = pd.read_sql(query, db_engine)

        # Get actual data types
        actual_schema = df_data.dtypes.to_dict()

        # Compare schemas
        mismatches = []
        for column, expected_dtype in expected_schema.items():
            if column not in actual_schema:
                mismatches.append(f"Column '{column}' not found in table")
                logger.error(f"Column '{column}' not found in table {table_name}")
            else:
                actual_dtype = str(actual_schema[column])
                # Normalize dtype comparison (int64 == int, float64 == float, object == str)
                if not (expected_dtype in actual_dtype or actual_dtype in expected_dtype):
                    mismatches.append(f"Column '{column}': expected {expected_dtype}, got {actual_dtype}")
                    logger.error(
                        f"Schema mismatch in {table_name}.{column}: expected {expected_dtype}, got {actual_dtype}")

        if mismatches:
            logger.error(f"Schema validation failed for {table_name}: {mismatches}")
            return False
        else:
            logger.info(f"Schema validation passed for {table_name}")
            return True

    except Exception as e:
        logger.error(f"Error while checking schema for table {table_name}: {e}")
        raise