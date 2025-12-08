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


@pytest.mark.dq
class TestDataQuality:

    # ========== DUPLICATE CHECKS FOR FILES ==========

    @pytest.mark.smoke
    def test_DQ_Sales_csv_duplicate_check(self):
        """Test duplicate check for sales_data CSV file - all columns"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_across_all_the_columns(
                "TestData/sales_data_linux.csv", "csv"
            )
            print(f"Duplicate status for sales_data: {duplicate_status}")

            assert duplicate_status, "There are duplicates in the sales data file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for sales_data failed: {e}")

    def test_DQ_Product_csv_duplicate_check(self):
        """Test duplicate check for product_data CSV file - all columns"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_across_all_the_columns(
                "TestData/product_data.csv", "csv"
            )
            print(f"Duplicate status for product_data: {duplicate_status}")

            assert duplicate_status, "There are duplicates in the product data file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for product_data failed: {e}")

    def test_DQ_Inventory_xml_duplicate_check(self):
        """Test duplicate check for inventory_data XML file - all columns"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_across_all_the_columns(
                "TestData/inventory_data.xml", "xml"
            )
            print(f"Duplicate status for inventory_data: {duplicate_status}")

            assert duplicate_status, "There are duplicates in the inventory data file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for inventory_data failed: {e}")

    def test_DQ_Supplier_json_duplicate_check(self):
        """Test duplicate check for supplier_data JSON file - all columns"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_across_all_the_columns(
                "TestData/supplier_data.json", "json"
            )
            print(f"Duplicate status for supplier_data: {duplicate_status}")

            assert duplicate_status, "There are duplicates in the supplier data file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for supplier_data failed: {e}")

    # ========== DUPLICATE CHECKS FOR SPECIFIC COLUMNS ==========

    def test_DQ_Sales_csv_duplicate_check_on_sales_id(self):
        """Test duplicate check for sales_data on sales_id column"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_for_specific_columns(
                "TestData/sales_data_linux.csv", "csv", ["sales_id"]
            )
            print(f"Duplicate status for sales_id: {duplicate_status}")

            assert duplicate_status, "There are duplicates in sales_id column"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for sales_id failed: {e}")

    def test_DQ_Product_csv_duplicate_check_on_product_id(self):
        """Test duplicate check for product_data on product_id column"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_for_specific_columns(
                "TestData/product_data.csv", "csv", ["product_id"]
            )
            print(f"Duplicate status for product_id: {duplicate_status}")

            assert duplicate_status, "There are duplicates in product_id column"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for product_id failed: {e}")

    # ========== DUPLICATE CHECKS FOR TARGET TABLES ==========

    def test_DQ_fact_sales_table_duplicate_check(self, connect_to_mysql_database):
        """Test duplicate check for fact_sales table - all columns"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_for_database_table(
                connect_to_mysql_database, "fact_sales"
            )
            print(f"Duplicate status for fact_sales: {duplicate_status}")

            assert duplicate_status, "There are duplicates in fact_sales table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for fact_sales failed: {e}")

    def test_DQ_fact_inventory_table_duplicate_check(self, connect_to_mysql_database):
        """Test duplicate check for fact_inventory table - all columns"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_for_database_table(
                connect_to_mysql_database, "fact_inventory"
            )
            print(f"Duplicate status for fact_inventory: {duplicate_status}")

            assert duplicate_status, "There are duplicates in fact_inventory table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for fact_inventory failed: {e}")

    def test_DQ_monthly_sales_summary_table_duplicate_check(self, connect_to_mysql_database):
        """Test duplicate check for monthly_sales_summary table - all columns"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_for_database_table(
                connect_to_mysql_database, "monthly_sales_summary"
            )
            print(f"Duplicate status for monthly_sales_summary: {duplicate_status}")

            assert duplicate_status, "There are duplicates in monthly_sales_summary table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for monthly_sales_summary failed: {e}")

    def test_DQ_inventory_levels_by_store_table_duplicate_check(self, connect_to_mysql_database):
        """Test duplicate check for inventory_levels_by_store table - all columns"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_for_database_table(
                connect_to_mysql_database, "inventory_levels_by_store"
            )
            print(f"Duplicate status for inventory_levels_by_store: {duplicate_status}")

            assert duplicate_status, "There are duplicates in inventory_levels_by_store table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for inventory_levels_by_store failed: {e}")

    # ========== DUPLICATE CHECKS FOR SPECIFIC COLUMNS IN TARGET TABLES ==========

    def test_DQ_fact_sales_table_duplicate_check_on_sales_id(self, connect_to_mysql_database):
        """Test duplicate check for fact_sales on sales_id column (PK check)"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            duplicate_status = check_for_duplicates_for_database_table(
                connect_to_mysql_database, "fact_sales", ["sales_id"]
            )
            print(f"Duplicate status for fact_sales.sales_id: {duplicate_status}")

            assert duplicate_status, "There are duplicates in fact_sales.sales_id column"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Duplicate check for fact_sales.sales_id failed: {e}")

    # ========== NULL VALUE CHECKS FOR FILES ==========

    @pytest.mark.smoke
    def test_DQ_Sales_csv_null_values_check(self):
        """Test null value check for sales_data CSV file"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            null_value_status = check_for_null_values(
                "TestData/sales_data_linux.csv", "csv"
            )
            logger.info(f"Is there a null in sales_data: {null_value_status}")

            assert null_value_status, "There are null values in the sales data file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Null check for sales_data failed: {e}")

    def test_DQ_Product_csv_null_values_check(self):
        """Test null value check for product_data CSV file"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            null_value_status = check_for_null_values(
                "TestData/product_data.csv", "csv"
            )
            logger.info(f"Is there a null in product_data: {null_value_status}")

            assert null_value_status, "There are null values in the product data file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Null check for product_data failed: {e}")

    def test_DQ_Inventory_xml_null_values_check(self):
        """Test null value check for inventory_data XML file"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            null_value_status = check_for_null_values(
                "TestData/inventory_data.xml", "xml"
            )
            logger.info(f"Is there a null in inventory_data: {null_value_status}")

            assert null_value_status, "There are null values in the inventory data file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Null check for inventory_data failed: {e}")

    def test_DQ_Supplier_json_null_values_check(self):
        """Test null value check for supplier_data JSON file"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            null_value_status = check_for_null_values(
                "TestData/supplier_data.json", "json"
            )
            logger.info(f"Is there a null in supplier_data: {null_value_status}")

            assert null_value_status, "There are null values in the supplier data file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Null check for supplier_data failed: {e}")

    # ========== NULL VALUE CHECKS FOR TARGET TABLES ==========

    def test_DQ_fact_sales_table_null_values_check(self, connect_to_mysql_database):
        """Test null value check for fact_sales table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            null_value_status = check_for_null_values_in_database_table(
                connect_to_mysql_database, "fact_sales"
            )
            logger.info(f"Is there a null in fact_sales: {null_value_status}")

            assert null_value_status, "There are null values in fact_sales table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Null check for fact_sales failed: {e}")

    def test_DQ_fact_inventory_table_null_values_check(self, connect_to_mysql_database):
        """Test null value check for fact_inventory table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            null_value_status = check_for_null_values_in_database_table(
                connect_to_mysql_database, "fact_inventory"
            )
            logger.info(f"Is there a null in fact_inventory: {null_value_status}")

            assert null_value_status, "There are null values in fact_inventory table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Null check for fact_inventory failed: {e}")

    def test_DQ_monthly_sales_summary_table_null_values_check(self, connect_to_mysql_database):
        """Test null value check for monthly_sales_summary table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            null_value_status = check_for_null_values_in_database_table(
                connect_to_mysql_database, "monthly_sales_summary"
            )
            logger.info(f"Is there a null in monthly_sales_summary: {null_value_status}")

            assert null_value_status, "There are null values in monthly_sales_summary table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Null check for monthly_sales_summary failed: {e}")

    def test_DQ_inventory_levels_by_store_table_null_values_check(self, connect_to_mysql_database):
        """Test null value check for inventory_levels_by_store table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            null_value_status = check_for_null_values_in_database_table(
                connect_to_mysql_database, "inventory_levels_by_store"
            )
            logger.info(f"Is there a null in inventory_levels_by_store: {null_value_status}")

            assert null_value_status, "There are null values in inventory_levels_by_store table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Null check for inventory_levels_by_store failed: {e}")

    # ========== FILE AVAILABILITY CHECKS ==========

    @pytest.mark.smoke
    def test_DQ_Sales_csv_file_availabilty(self):
        """Test file availability for sales_data CSV"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            assert check_file_existence("TestData/sales_data_linux.csv"), \
                "sales_data_linux.csv file does not exist in location"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"File availability check for sales_data failed: {e}")

    def test_DQ_Product_csv_file_availabilty(self):
        """Test file availability for product_data CSV"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            assert check_file_existence("TestData/product_data.csv"), \
                "product_data.csv file does not exist in location"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"File availability check for product_data failed: {e}")

    def test_DQ_Inventory_xml_file_availabilty(self):
        """Test file availability for inventory_data XML"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            assert check_file_existence("TestData/inventory_data.xml"), \
                "inventory_data.xml file does not exist in location"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"File availability check for inventory_data failed: {e}")

    def test_DQ_Supplier_json_file_availabilty(self):
        """Test file availability for supplier_data JSON"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            assert check_file_existence("TestData/supplier_data.json"), \
                "supplier_data.json file does not exist in location"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"File availability check for supplier_data failed: {e}")

    # ========== FILE SIZE CHECKS ==========

    def test_DQ_Sales_csv_file_size_check(self):
        """Test file size check for sales_data CSV"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            assert check_file_size("TestData/sales_data_linux.csv"), \
                "sales_data_linux.csv is a zero byte file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"File size check for sales_data failed: {e}")

    def test_DQ_Product_csv_file_size_check(self):
        """Test file size check for product_data CSV"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            assert check_file_size("TestData/product_data.csv"), \
                "product_data.csv is a zero byte file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"File size check for product_data failed: {e}")

    def test_DQ_Inventory_xml_file_size_check(self):
        """Test file size check for inventory_data XML"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            assert check_file_size("TestData/inventory_data.xml"), \
                "inventory_data.xml is a zero byte file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"File size check for inventory_data failed: {e}")

    def test_DQ_Supplier_json_file_size_check(self):
        """Test file size check for supplier_data JSON"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            assert check_file_size("TestData/supplier_data.json"), \
                "supplier_data.json is a zero byte file"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"File size check for supplier_data failed: {e}")

    # ========== REFERENTIAL INTEGRITY CHECKS ==========

    def test_DQ_Referential_Integrity_fact_sales_to_product(self, connect_to_mysql_database):
        """Test referential integrity: fact_sales.product_id -> staging_product.product_id"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            integrity_status = check_referential_integrity(
                connect_to_mysql_database,
                "staging_product", "product_id",
                "fact_sales", "product_id"
            )

            assert integrity_status, \
                "Referential integrity violation: fact_sales.product_id has orphan records"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Referential integrity check failed: {e}")

    def test_DQ_Referential_Integrity_fact_sales_to_stores(self, connect_to_mysql_database):
        """Test referential integrity: fact_sales.store_id -> staging_stores.store_id"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            integrity_status = check_referential_integrity(
                connect_to_mysql_database,
                "staging_stores", "store_id",
                "fact_sales", "store_id"
            )

            assert integrity_status, \
                "Referential integrity violation: fact_sales.store_id has orphan records"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Referential integrity check failed: {e}")

    def test_DQ_Referential_Integrity_fact_inventory_to_product(self, connect_to_mysql_database):
        """Test referential integrity: fact_inventory.product_id -> staging_product.product_id"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            integrity_status = check_referential_integrity(
                connect_to_mysql_database,
                "staging_product", "product_id",
                "fact_inventory", "product_id"
            )

            assert integrity_status, \
                "Referential integrity violation: fact_inventory.product_id has orphan records"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Referential integrity check failed: {e}")

    def test_DQ_Referential_Integrity_fact_inventory_to_stores(self, connect_to_mysql_database):
        """Test referential integrity: fact_inventory.store_id -> staging_stores.store_id"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            integrity_status = check_referential_integrity(
                connect_to_mysql_database,
                "staging_stores", "store_id",
                "fact_inventory", "store_id"
            )

            assert integrity_status, \
                "Referential integrity violation: fact_inventory.store_id has orphan records"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Referential integrity check failed: {e}")

    # ========== SCHEMA / DATA TYPE VALIDATION ==========

    def test_DQ_Schema_Validation_fact_sales(self, connect_to_mysql_database):
        """Test schema validation for fact_sales table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            expected_schema = {
                'sales_id': 'int',
                'product_id': 'int',
                'store_id': 'int',
                'quantity': 'int',
                'total_sales': 'float',
                'sale_date': 'object'  # Date stored as object in pandas
            }

            schema_status = check_data_type_schema(
                connect_to_mysql_database, "fact_sales", expected_schema
            )

            assert schema_status, "Schema validation failed for fact_sales table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Schema validation for fact_sales failed: {e}")

    def test_DQ_Schema_Validation_fact_inventory(self, connect_to_mysql_database):
        """Test schema validation for fact_inventory table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            expected_schema = {
                'product_id': 'int',
                'store_id': 'int',
                'quantity_on_hand': 'int',
                'last_updated': 'object'
            }

            schema_status = check_data_type_schema(
                connect_to_mysql_database, "fact_inventory", expected_schema
            )

            assert schema_status, "Schema validation failed for fact_inventory table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Schema validation for fact_inventory failed: {e}")

    def test_DQ_Schema_Validation_monthly_sales_summary(self, connect_to_mysql_database):
        """Test schema validation for monthly_sales_summary table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            expected_schema = {
                'product_id': 'int',
                'month': 'int',
                'year': 'int',
                'total_sales': 'float'
            }

            schema_status = check_data_type_schema(
                connect_to_mysql_database, "monthly_sales_summary", expected_schema
            )

            assert schema_status, "Schema validation failed for monthly_sales_summary table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Schema validation for monthly_sales_summary failed: {e}")

    def test_DQ_Schema_Validation_inventory_levels_by_store(self, connect_to_mysql_database):
        """Test schema validation for inventory_levels_by_store table"""
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case '{test_case_name}' execution has started...")

            expected_schema = {
                'store_id': 'int',
                'total_inventory': 'int'
            }

            schema_status = check_data_type_schema(
                connect_to_mysql_database, "inventory_levels_by_store", expected_schema
            )

            assert schema_status, "Schema validation failed for inventory_levels_by_store table"

            logger.info(f"Test case '{test_case_name}' execution has completed...")
        except Exception as e:
            logger.error(f"Test case '{test_case_name}' execution has failed: {e}")
            pytest.fail(f"Schema validation for inventory_levels_by_store failed: {e}")