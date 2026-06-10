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
    
    # 检查是否已有 shuhu 账号
    cursor.execute("SELECT id FROM users WHERE username = ?", ('shuhu',))
    existing = cursor.fetchone()
    
    if not existing:
        password_hash = bcrypt.hashpw('Hu200692?'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ('shuhu', password_hash.decode('utf-8'))
        )
        print("用户 shuhu 创建成功!")
    else:
        print("用户 shuhu 已存在，跳过创建。")
    
    conn.commit()
    conn.close()
    print("数据库初始化完成! (ctf_blog.db)")

if __name__ == '__main__':
    init_db()
