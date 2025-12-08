import pandas as pd
from sqlalchemy import create_engine
import oracledb
import paramiko
import pytest
import inspect
from CommonUtilities.utilities import *

import logging

# Logging configuration
logging.basicConfig(
    filename="Logs/etljob.log",
    filemode="w",
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@pytest.mark.regression
class TestDataLoading:

    @pytest.mark.smoke
    def test_DL_Monthly_sales_summary(self, connect_to_mysql_database):
        """Test monthly sales summary load from intermediate to final table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            query_expected = """SELECT product_id, year, month, total_sales 
                               FROM intermediate_monthly_sales_summary_source 
                               ORDER BY product_id, year, month"""

            query_actual = """SELECT product_id, year, month, total_sales 
                             FROM monthly_sales_summary 
                             ORDER BY product_id, year, month"""

            verify_expected_as_database_to_actual_as_database(
                connect_to_mysql_database, query_expected,
                connect_to_mysql_database, query_actual
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")

    @pytest.mark.smoke
    def test_DL_fact_Sales(self, connect_to_mysql_database):
        """Test fact_sales load from intermediate_filtered_sales"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            query_expected = """SELECT sales_id, product_id, store_id, quantity, total_sales, sale_date
                               FROM intermediate_filtered_sales 
                               ORDER BY sales_id"""

            query_actual = """SELECT sales_id, product_id, store_id, quantity, total_sales, sale_date
                             FROM fact_sales 
                             ORDER BY sales_id"""

            verify_expected_as_database_to_actual_as_database(
                connect_to_mysql_database, query_expected,
                connect_to_mysql_database, query_actual
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")

    def test_DL_fact_inventory(self, connect_to_mysql_database):
        """Test fact_inventory load from staging_inventory"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            query_expected = """SELECT product_id, store_id, quantity_on_hand, last_updated
                               FROM staging_inventory 
                               ORDER BY product_id, store_id"""

            query_actual = """SELECT product_id, store_id, quantity_on_hand, last_updated
                             FROM fact_inventory 
                             ORDER BY product_id, store_id"""

            verify_expected_as_database_to_actual_as_database(
                connect_to_mysql_database, query_expected,
                connect_to_mysql_database, query_actual
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")

    def test_DL_inventory_level_by_stores(self, connect_to_mysql_database):
        """Test inventory_levels_by_store load from intermediate_aggregated_inventory_level"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            query_expected = """SELECT store_id, total_inventory
                               FROM intermediate_aggregated_inventory_level 
                               ORDER BY store_id"""

            query_actual = """SELECT store_id, total_inventory
                             FROM inventory_levels_by_store 
                             ORDER BY store_id"""

            verify_expected_as_database_to_actual_as_database(
                connect_to_mysql_database, query_expected,
                connect_to_mysql_database, query_actual
            )

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Test case '{test_case_name}' failed")