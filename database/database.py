import os
import re
import mysql.connector
from dotenv import load_dotenv

# load credentials.env relative to this file's folder
env_path = os.path.join(os.path.dirname(__file__), "credentials.env")
load_dotenv(env_path)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "Insyra_db")


def sanitize_identifier(name):
    """Ensure database identifier contains only valid alphanumeric characters."""
    if not name or not re.match(r"^[A-Za-z0-9_]+$", name):
        raise ValueError(f"Invalid database identifier: {name}")
    return name


def get_conn():
    """Establish and return a connection to MySQL database."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=3306,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connection_timeout=5
    )
    return conn


def init_database():
    """
    Creates the database and dataset_logs table if they don't exist yet.
    Safe to run on every startup.
    """
    try:
        clean_db_name = sanitize_identifier(DB_NAME)

        # connect without database first to ensure database exists
        server_conn = mysql.connector.connect(
            host=DB_HOST,
            port=3306,
            user=DB_USER,
            password=DB_PASSWORD,
            connection_timeout=5
        )
        cursor = server_conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{clean_db_name}`;")
        cursor.close()
        server_conn.close()

        # now connect to the specific database and create table
        conn = get_conn()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS dataset_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_name VARCHAR(255) NOT NULL,
            original_rows INT,
            cleaned_rows INT,
            rows_removed INT,
            saved_path VARCHAR(255),
            status VARCHAR(50) DEFAULT 'SUCCESS',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("[Database Notice] Could not initialize database:", e)
        return False


def log_dataset_action(file_name, original_rows, cleaned_rows, rows_removed, saved_path):
    """Logs a completed dataset cleaning operation into MySQL using parameterized queries."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        query = """
        INSERT INTO dataset_logs (file_name, original_rows, cleaned_rows, rows_removed, saved_path)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(query, (file_name, original_rows, cleaned_rows, rows_removed, saved_path))
        conn.commit()
        log_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"[Database] Logged cleaning record (ID: {log_id}) to MySQL.")
        return log_id
    except Exception as e:
        print("[Database Notice] Could not save log to MySQL:", e)
        return None


def get_dataset_logs(limit=10):
    """Fetches recent dataset activity logs from MySQL using parameterized limit."""
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM dataset_logs ORDER BY created_at DESC LIMIT %s;"
        cursor.execute(query, (int(limit),))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    except Exception as e:
        print("[Database Notice] Could not fetch logs from MySQL:", e)
        return []


if __name__ == "__main__":
    print("Testing MySQL connection and table setup...")
    success = init_database()
    if success:
        print("Database and table 'dataset_logs' are ready!")
    else:
        print("Please verify MySQL server is running on port 3306.")
