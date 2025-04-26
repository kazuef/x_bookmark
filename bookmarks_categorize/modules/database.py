import sqlite3, os
from contextlib import contextmanager

base_path = os.path.dirname(__file__)
db_path = os.path.join(base_path, "../db/bookmarks.db")

@contextmanager
def get_connection():
    """
    DB への接続を取得し、処理後に必ずクローズするコンテキストマネージャー
    """
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    # dbディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブルがなければ作成（初回実行時）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks_category (
            id INTEGER NOT NULL PRIMARY KEY,
            categorize_name TEXT NOT NULL UNIQUE,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            is_deleted INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            id TEXT NOT NULL PRIMARY KEY,
            categorize_id INTEGER NOT NULL DEFAULT 0,
            tweet TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            is_deleted INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (categorize_id) REFERENCES bookmarks_category(id)
        )
    """)

    conn.commit()
    print("DB作成完了")
    conn.close()
