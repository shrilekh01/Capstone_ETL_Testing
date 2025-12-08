import pandas as pd
from sqlalchemy import create_engine
import oracledb
import paramiko
import pytest
import inspect
from CommonUtilities.utilities import *

import logging

# Logging configution
logging.basicConfig(
    filename="Logs/etljob.log",
    filemode="w",
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@pytest.mark.regression
class TestDataExtraction:

    @pytest.mark.smoke
    def test_DE_from_sales_data_between_source_and_staging(self, connect_to_mysql_database):
        """Test sales data extraction from CSV to staging_sales"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            verify_expected_as_file_to_actual_as_database(
                "TestData/sales_data_linux.csv",
                "csv",
                connect_to_mysql_database,
                "staging_sales",
                test_case_name=test_case_name
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")

    @pytest.mark.smoke
    def test_DE_from_product_data_between_source_and_staging(self, connect_to_mysql_database):
        """Test product data extraction from CSV to staging_product"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            verify_expected_as_file_to_actual_as_database(
                "TestData/product_data.csv",
                "csv",
                connect_to_mysql_database,
                "staging_product",
                test_case_name=test_case_name
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")

    def test_DE_from_supplier_data_between_source_and_staging(self, connect_to_mysql_database):
        """Test supplier data extraction from JSON to staging_supplier"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            verify_expected_as_file_to_actual_as_database(
                "TestData/supplier_data.json",
                "json",
                connect_to_mysql_database,
                "staging_supplier",
                test_case_name=test_case_name
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")

    def test_DE_from_inventory_data_between_source_and_staging(self, connect_to_mysql_database):
        """Test inventory data extraction from XML to staging_inventory"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            verify_expected_as_file_to_actual_as_database(
                "TestData/inventory_data.xml",
                "xml",
                connect_to_mysql_database,
                "staging_inventory",
                test_case_name=test_case_name
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")

    def test_DE_from_stores_data_between_source_and_staging(self, connect_to_oracle_database,
                                                            connect_to_mysql_database):
        """Test stores data extraction from Oracle to MySQL staging_stores"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            query_expected = """SELECT * FROM stores ORDER BY store_id"""
            query_actual = """SELECT * FROM staging_stores ORDER BY store_id"""

            verify_expected_as_database_to_actual_as_database(
                connect_to_oracle_database, query_expected,
                connect_to_mysql_database, query_actual
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")