import pandas as pd
from sqlalchemy import create_engine
import oracledb
import psycopg2
import pymysql
from CommonUtilities.utilities import CommonUtilities
from Configuration.etlconfig import *
import logging


# Logging configuration
logging.basicConfig(
    filename="Logs/etljob.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# oracle_engine = create_engine(
#     "oracle+oracledb://system:sunbeam@localhost:1521/?service_name=FREEPDB1"
# )

oracle_engine = create_engine(
    f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/?service_name={ORACLE_SERVICE}"
)

# PostgreSQL (AWS RDS) engine
postgres_engine = create_engine(
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


# MySQL engine
mysql_engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)


class DataExtraction:

    # 1. Extract sales data from LINUX server
    def extract_sales_data(self):
        logger.info("Sales data extraction started...")
        try:
            util = CommonUtilities()
            util.sales_data_from_linux_server()

            
            df = pd.read_csv("TestData/sales_data_linux.csv")  
            df.to_sql("staging_sales", mysql_engine, index=False, if_exists="replace")

            logger.info("Sales data extraction completed successfully.")
        except Exception as e:
            logger.error(f"Error during sales data extraction: {e}", exc_info=True)

    # 2. Extract product data
    def extract_product_data_and_load_stage(self):
        logger.info("Product data extraction started...")
        try:
            df = pd.read_csv("SourceSystem/product_data.csv")
            df.to_sql("staging_product", mysql_engine, index=False, if_exists="replace")

            logger.info("Product data extraction completed successfully.")
        except Exception as e:
            logger.error(f"Error during product data extraction: {e}", exc_info=True)

    # 3. Extract inventory data
    def extract_inventory_data_and_load_stage(self):
        logger.info("Inventory data extraction started...")
        try:
            df = pd.read_xml("SourceSystem/inventory_data.xml", xpath=".//item")
            df.to_sql("staging_inventory", mysql_engine, index=False, if_exists="replace")

            logger.info("Inventory data extraction completed successfully.")
        except Exception as e:
            logger.error(f"Error during inventory data extraction: {e}", exc_info=True)

    # 4. Extract supplier data
    def extract_supplier_data_and_load_stage(self):
        logger.info("Supplier data extraction started...")
        try:
            df = pd.read_json("SourceSystem/supplier_data.json")
            df.to_sql("staging_supplier", mysql_engine, index=False, if_exists="replace")

            logger.info("Supplier data extraction completed successfully.")
        except Exception as e:
            logger.error(f"Error during supplier data extraction: {e}", exc_info=True)

    # 5. Extract Oracle stores table
    def extract_stores_data_and_load_stage(self):
        logger.info("Stores data extraction started...")
        try:
            print("inside try ")
            df = pd.read_sql("SELECT * FROM stores", oracle_engine)
            count = len(df)  # Fixed: use len() for DataFrame
            print(f"Store count: {count}")
            print("data from oracle stores fetched")
            df.to_sql("staging_stores", mysql_engine, index=False, if_exists="replace")
            logger.info("Stores data extraction completed successfully.")
        except Exception as e:
            logger.error(f"Error during stores data extraction: {e}", exc_info=True)
            logger.info("Stores data extraction completed successfully.")
        except Exception as e:
            logger.error(f"Error during stores data extraction: {e}", exc_info=True)
    #
    # # 5. Extract postgre stores table
    # def extract_stores_data_and_load_stage(self):
    #     logger.info("Stores data extraction started...")
    #     try:
    #         df = pd.read_sql("SELECT store_id, store_name FROM stores", postgres_engine)
    #         df.to_sql("staging_stores", mysql_engine, index=False, if_exists="replace")
    #         logger.info("Stores data extraction completed successfully.")
    #     except Exception as e:
    #         logger.error(f"Error during stores data extraction: {e}", exc_info=True)


if __name__ == "__main__":
    de = DataExtraction()
    de.extract_sales_data()
    de.extract_product_data_and_load_stage()
    de.extract_inventory_data_and_load_stage()
    de.extract_supplier_data_and_load_stage()
    de.extract_stores_data_and_load_stage()

    print("success")

