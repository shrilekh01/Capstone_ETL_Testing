# Oracle database
ORACLE_USER = "system"
ORACLE_PASSWORD = "sunbeam"
ORACLE_HOST = "localhost"
ORACLE_PORT = 1521
ORACLE_SERVICE = "FREEPDB1"

# mysql database
# mysql database
MYSQL_USER = os.getenv("MYSQL_USER", "root")  # Default to 'root' if env var not set
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "sunbeam")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")  # Can be overridden in CI
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "retaildwh")
# Linux server
hostname = "192.168.56.103"
username = "root"
password = "root"
remote_file_path = "/root/sales_data.csv"
local_file_path = "SourceSystem/sales_data_linux.csv"

# postgre sql
POSTGRES_USER = "capstone"
POSTGRES_PASSWORD = "capstone"
POSTGRES_HOST = "capstone2.cra4maemeqqs.ap-south-1.rds.amazonaws.com"
POSTGRES_PORT = 5432
POSTGRES_DB = "capstone_src"


