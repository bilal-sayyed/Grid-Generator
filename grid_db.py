import sqlite3
import os
import json
from hashlib import md5
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), "grids.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS grids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            hash TEXT UNIQUE,
            timestamp TEXT,
            json TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_grid(grid):
    flat = ''.join([''.join(row) for row in grid])
    return md5(flat.encode()).hexdigest()

def is_duplicate(grid_hash):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT filename FROM grids WHERE hash = ?", (grid_hash,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_grid_to_db(filename, grid):
    grid_hash = hash_grid(grid)
    duplicate = is_duplicate(grid_hash)
    if duplicate:
        print(f"❌ Duplicate detected!")
        print(f"🔁 Tried to save: {filename}")
        print(f"📁 Already exists as: {duplicate}")
        return False


    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO grids (filename, hash, timestamp, json)
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        grid_hash,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        json.dumps(grid)
    ))
    conn.commit()
    conn.close()
    print(f"✅ Grid saved to DB: {filename}")
    return True
