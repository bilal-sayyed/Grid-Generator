import mysql.connector
import json
import os

DB_HOST = os.getenv("MYSQLHOST", "your-host")
DB_USER = os.getenv("MYSQLUSER", "your-user")
DB_PASSWORD = os.getenv("MYSQLPASSWORD", "your-password")
DB_NAME = os.getenv("MYSQLDATABASE", "your-database")
DB_PORT = int(os.getenv("MYSQLPORT", "3306"))

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
