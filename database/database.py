import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("database/credentials.env")
def get_conn():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        connection_timeout=10
    )

    return conn
