import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'ctf_blog.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute("SELECT id FROM users WHERE username = ?", ('',))
    existing = cursor.fetchone()
    
    if not existing:
        password_hash = bcrypt.hashpw(''.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ('shuhu', password_hash.decode('utf-8'))
        )
        print("")
    else:
        print("")
    
    conn.commit()
    conn.close()
    print("")

if __name__ == '__main__':
    init_db()
