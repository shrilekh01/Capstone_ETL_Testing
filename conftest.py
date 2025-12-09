import pandas as pd
import pytest
from sqlalchemy import create_engine
import oracledb
import paramiko

from Configuration.etlconfig import *
import logging
import sys

# Logging configuration
logging.basicConfig(
    filename="Logs/etljob.log",
    filemode="w",
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Oracle client in thin mode (no Oracle Instant Client required)
# This allows connection without local Oracle installation
try:
    # For oracledb version 1.x and above, thin mode is the default
    # No need for init_oracle_client() unless you want thick mode
    # Remove or comment out the next line to use thin mode (recommended for CI/CD)
    # oracledb.init_oracle_client()  # Only uncomment if you have Oracle Instant Client installed

    # Alternative: Initialize with config_dir parameter if needed
    # oracledb.init_oracle_client(config_dir="/opt/oracle/network/admin")

    logger.info("Oracle driver initialized successfully")
except Exception as e:
    logger.warning(f"Oracle client initialization note: {e}")
    logger.info("Using thin mode - Oracle Instant Client not required")


@pytest.fixture()
def connect_to_oracle_database():
    """Fixture to connect to Oracle database using oracledb driver"""
    logger.info("Oracle database connection is being established...")
    try:
        # Connection string for oracledb (thin mode)
        # Thin mode doesn't require Oracle Instant Client
        connection_string = f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/?service_name={ORACLE_SERVICE}"

        logger.info(f"Connecting to Oracle with: {ORACLE_USER}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")

        # Create SQLAlchemy engine with oracledb
        oracle_engine = create_engine(
            connection_string,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600  # Recycle connections after 1 hour
        )

        # Test the connection
        with oracle_engine.connect() as conn:
            logger.info("Oracle database connection test successful")

        logger.info("Oracle database connection has been established.")
        yield oracle_engine

    except Exception as e:
        logger.error(f"Failed to connect to Oracle database: {str(e)}")
        logger.error(f"Connection details: {ORACLE_USER}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")

        # Provide helpful error messages
        if "DPI-1047" in str(e) or "Cannot locate a 64-bit Oracle Client library" in str(e):
            logger.error("Oracle Instant Client missing. Solutions:")
            logger.error("1. Install Oracle Instant Client (for thick mode)")
            logger.error("2. Use thin mode by NOT calling init_oracle_client()")
            logger.error("3. Check LD_LIBRARY_PATH environment variable")

        pytest.skip(f"Skipping Oracle tests: {e}")
        yield None  # Return None if connection fails
    finally:
        if 'oracle_engine' in locals():
            oracle_engine.dispose()
            logger.info("Oracle database connection has been closed.")


@pytest.fixture()
def connect_to_mysql_database():
    """Fixture to connect to MySQL database"""
    logger.info("MySQL database connection is being established...")
    try:
        mysql_engine = create_engine(
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}",
            pool_pre_ping=True,
            pool_recycle=3600
        )

        # Test the connection
        with mysql_engine.connect() as conn:
            logger.info("MySQL database connection test successful")

        logger.info("MySQL database connection has been established.")
        yield mysql_engine

    except Exception as e:
        logger.error(f"Failed to connect to MySQL database: {e}")
        pytest.skip(f"Skipping MySQL tests: {e}")
        yield None
    finally:
        if 'mysql_engine' in locals():
            mysql_engine.dispose()
            logger.info("MySQL database connection has been closed.")