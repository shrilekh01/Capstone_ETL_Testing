import pandas as pd
import pytest
from sqlalchemy import create_engine
import oracledb
import paramiko
import os
import logging

# Import configuration - will be overridden for CI if needed
from Configuration.etlconfig import *
import sys

# Logging configuration
logging.basicConfig(
    filename="Logs/etljob.log",
    filemode="w",
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====================================================
# ENVIRONMENT DETECTION & CONFIGURATION OVERRIDE
# ====================================================

def get_mysql_config():
    """
    Get MySQL configuration based on environment.
    Returns appropriate config for CI vs local development.
    """
    # Check if we're running in GitHub Actions CI
    if os.getenv('GITHUB_ACTIONS') == 'true':
        logger.info("Running in GitHub Actions CI environment")
        
        # CI Environment Configuration
        config = {
            'MYSQL_HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),  # Container IP for CI
            'MYSQL_USER': os.getenv('MYSQL_USER', 'root'),
            'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD', 'root'),
            'MYSQL_PORT': int(os.getenv('MYSQL_PORT', '3306')),
            'MYSQL_DATABASE': os.getenv('MYSQL_DATABASE', 'retaildwh'),
            
            # Skip external services in CI (tests will be skipped)
            'ORACLE_HOST': None,
            'ORACLE_USER': None,
            'ORACLE_PASSWORD': None,
            'ORACLE_PORT': None,
            'ORACLE_SERVICE': None,
            
            # Skip Linux server in CI
            'hostname': None,
            'username': None,
            'password': None,
            'remote_file_path': None,
            'local_file_path': None,
            
            'IS_CI': True
        }
        
        logger.info(f"CI MySQL config: {config['MYSQL_USER']}@{config['MYSQL_HOST']}:{config['MYSQL_PORT']}/{config['MYSQL_DATABASE']}")
        return config
    
    else:
        # Local Development - use configuration from etlconfig.py
        logger.info("Running in local development environment")
        config = {
            'MYSQL_HOST': MYSQL_HOST,
            'MYSQL_USER': MYSQL_USER,
            'MYSQL_PASSWORD': MYSQL_PASSWORD,
            'MYSQL_PORT': MYSQL_PORT,
            'MYSQL_DATABASE': MYSQL_DATABASE,
            
            'ORACLE_HOST': ORACLE_HOST,
            'ORACLE_USER': ORACLE_USER,
            'ORACLE_PASSWORD': ORACLE_PASSWORD,
            'ORACLE_PORT': ORACLE_PORT,
            'ORACLE_SERVICE': ORACLE_SERVICE,
            
            'hostname': hostname,
            'username': username,
            'password': password,
            'remote_file_path': remote_file_path,
            'local_file_path': local_file_path,
            
            'IS_CI': False
        }
        
        logger.info(f"Local MySQL config: {config['MYSQL_USER']}@{config['MYSQL_HOST']}:{config['MYSQL_PORT']}/{config['MYSQL_DATABASE']}")
        return config

# Get configuration based on environment
CONFIG = get_mysql_config()

# ====================================================
# ORACLE CLIENT INITIALIZATION
# ====================================================

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

# ====================================================
# DATABASE FIXTURES
# ====================================================

@pytest.fixture()
def connect_to_oracle_database():
    """Fixture to connect to Oracle database using oracledb driver"""
    
    # Skip Oracle tests in CI environment
    if CONFIG['IS_CI'] or not CONFIG['ORACLE_HOST']:
        logger.info("Skipping Oracle tests - not available in CI or disabled")
        pytest.skip("Oracle database not available in CI environment")
        yield None
        return
    
    logger.info("Oracle database connection is being established...")
    try:
        # Connection string for oracledb (thin mode)
        # Thin mode doesn't require Oracle Instant Client
        connection_string = f"oracle+oracledb://{CONFIG['ORACLE_USER']}:{CONFIG['ORACLE_PASSWORD']}@{CONFIG['ORACLE_HOST']}:{CONFIG['ORACLE_PORT']}/?service_name={CONFIG['ORACLE_SERVICE']}"

        logger.info(f"Connecting to Oracle with: {CONFIG['ORACLE_USER']}@{CONFIG['ORACLE_HOST']}:{CONFIG['ORACLE_PORT']}/{CONFIG['ORACLE_SERVICE']}")

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
        logger.error(f"Connection details: {CONFIG['ORACLE_USER']}@{CONFIG['ORACLE_HOST']}:{CONFIG['ORACLE_PORT']}/{CONFIG['ORACLE_SERVICE']}")

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
    
    # Debug logging for connection details
    logger.info(f"MySQL Connection Details:")
    logger.info(f"  Host: {CONFIG['MYSQL_HOST']}")
    logger.info(f"  Port: {CONFIG['MYSQL_PORT']}")
    logger.info(f"  Database: {CONFIG['MYSQL_DATABASE']}")
    logger.info(f"  User: {CONFIG['MYSQL_USER']}")
    logger.info(f"  Environment: {'CI' if CONFIG['IS_CI'] else 'Local'}")
    
    try:
        # Build connection string
        connection_string = (
            f"mysql+pymysql://{CONFIG['MYSQL_USER']}:{CONFIG['MYSQL_PASSWORD']}"
            f"@{CONFIG['MYSQL_HOST']}:{CONFIG['MYSQL_PORT']}/{CONFIG['MYSQL_DATABASE']}"
        )
        
        logger.info(f"MySQL Connection String: mysql+pymysql://{CONFIG['MYSQL_USER']}:****@{CONFIG['MYSQL_HOST']}:{CONFIG['MYSQL_PORT']}/{CONFIG['MYSQL_DATABASE']}")

        # Create SQLAlchemy engine
        mysql_engine = create_engine(
            connection_string,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,   # Recycle connections after 1 hour
            connect_args={
                'connect_timeout': 10  # 10 second connection timeout
            }
        )

        # Test the connection
        logger.info("Testing MySQL connection...")
        with mysql_engine.connect() as conn:
            # Try a simple query to verify connection
            result = conn.execute("SELECT 1 as test")
            test_value = result.scalar()
            logger.info(f"MySQL database connection test successful: SELECT 1 = {test_value}")
            
            # Log MySQL version for debugging
            try:
                version_result = conn.execute("SELECT VERSION()")
                mysql_version = version_result.scalar()
                logger.info(f"MySQL Server Version: {mysql_version}")
            except:
                logger.info("Could not retrieve MySQL version")

        logger.info("MySQL database connection has been established.")
        yield mysql_engine

    except Exception as e:
        logger.error(f"Failed to connect to MySQL database: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        
        # Provide helpful debug information
        if "Connection refused" in str(e):
            logger.error("Connection refused. Possible issues:")
            logger.error("1. MySQL server is not running")
            logger.error("2. Wrong host/port configuration")
            logger.error(f"3. Trying to connect to: {CONFIG['MYSQL_HOST']}:{CONFIG['MYSQL_PORT']}")
            
            if CONFIG['IS_CI']:
                logger.error("CI Environment Notes:")
                logger.error("- In GitHub Actions, use '127.0.0.1' not 'localhost'")
                logger.error("- Ensure MySQL service is defined in workflow")
                logger.error("- Check if port 3306 is exposed")
        
        pytest.skip(f"Skipping MySQL tests: {e}")
        yield None  # Return None if connection fails
    finally:
        if 'mysql_engine' in locals():
            mysql_engine.dispose()
            logger.info("MySQL database connection has been closed.")

# ====================================================
# HELPER FUNCTION FOR TEST DEBUGGING
# ====================================================

def print_environment_info():
    """Helper function to print environment information for debugging"""
    print("\n" + "="*60)
    print("ENVIRONMENT CONFIGURATION")
    print("="*60)
    print(f"Environment: {'GitHub Actions CI' if CONFIG['IS_CI'] else 'Local Development'}")
    print(f"MYSQL_HOST: {CONFIG['MYSQL_HOST']}")
    print(f"MYSQL_PORT: {CONFIG['MYSQL_PORT']}")
    print(f"MYSQL_DATABASE: {CONFIG['MYSQL_DATABASE']}")
    print(f"MYSQL_USER: {CONFIG['MYSQL_USER']}")
    print(f"ORACLE Available: {CONFIG['ORACLE_HOST'] is not None}")
    print(f"Linux Server Available: {CONFIG['hostname'] is not None}")
    print("="*60 + "\n")

# Call this function when module loads for debugging
if __name__ == "__main__":
    print_environment_info()
