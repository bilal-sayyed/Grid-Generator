from dotenv import load_dotenv
load_dotenv()

import json
import os
import mysql.connector
from urllib.parse import urlparse


# Get the URL as a string
mysql_url = os.getenv("MYSQL_URL")

if not mysql_url:
    raise ValueError("mysql://root:QRPdZNXyflqGGlgkXQUnkiKdUuUfXFIW@mysql.railway.internal:3306/railway environment variable not set.")

# Parse it
url = urlparse(mysql_url)

# Extract connection details
DB_HOST = url.hostname
DB_USER = url.username
DB_PASSWORD = url.password
DB_NAME = url.path.lstrip("/")
DB_PORT = url.port or 3306

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )


def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grids (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                grid LONGTEXT
            )
        ''')
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def save_grid_to_db(filename, grid):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        grid_json = json.dumps(grid)
        cursor.execute('''
            INSERT INTO grids (filename, grid) VALUES (%s, %s)
        ''', (filename, grid_json))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
