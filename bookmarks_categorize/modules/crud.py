import os
import json
import uuid
from .database import db_path, get_connection

def get_or_create_category(name: str) -> int:
    """
    カテゴリ名で検索し、存在しなければ新規作成してIDを返す
    
    Args:
        name: カテゴリ名
        
    Returns:
        int: カテゴリID
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM bookmarks_category WHERE categorize_name = ?", (name,))
            row = cur.fetchone()
            if row:
                category_id = row[0]
            else:
                cur.execute("INSERT INTO bookmarks_category (categorize_name) VALUES (?)", (name,))
                category_id = cur.lastrowid
                conn.commit()
            return category_id
        except Exception as e:
            conn.rollback()
            raise e

def insert_bookmark(bookmark_id: str, categorize_id: int, tweet: dict):
    """
    ブックマークをデータベースに挿入する
    
    Args:
        bookmark_id: ブックマークの一意識別子
        categorize_id: カテゴリID
        tweet: ツイート内容の辞書
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            tweet_json = json.dumps(tweet, ensure_ascii=False)
            cur.execute(
                "INSERT OR IGNORE INTO bookmarks (id, categorize_id, tweet) VALUES (?, ?, ?)",
                (bookmark_id, categorize_id, tweet_json)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

def get_bookmarks_by_category(category_id: int = None):
    """
    カテゴリIDに基づいてブックマークを取得する
    
    Args:
        category_id: カテゴリID（Noneの場合は全て取得）
        
    Returns:
        list: ブックマークのリスト
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            if category_id is not None:
                cur.execute("""
                    SELECT b.id, c.categorize_name, b.tweet, b.created_at 
                    FROM bookmarks b
                    JOIN bookmarks_category c ON b.categorize_id = c.id
                    WHERE b.categorize_id = ? AND b.is_deleted = 0
                    ORDER BY b.created_at DESC
                """, (category_id,))
            else:
                cur.execute("""
                    SELECT b.id, c.categorize_name, b.tweet, b.created_at 
                    FROM bookmarks b
                    JOIN bookmarks_category c ON b.categorize_id = c.id
                    WHERE b.is_deleted = 0
                    ORDER BY b.created_at DESC
                """)
            
            rows = cur.fetchall()
            bookmarks = []
            for row in rows:
                bookmark = {
                    "id": row[0],
                    "category": row[1],
                    "tweet": json.loads(row[2]),
                    "created_at": row[3]
                }
                bookmarks.append(bookmark)
            return bookmarks
        except Exception as e:
            raise e

def get_all_categories():
    """
    全てのカテゴリを取得する
    
    Returns:
        list: カテゴリのリスト
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, categorize_name, created_at
                FROM bookmarks_category
                WHERE is_deleted = 0
                ORDER BY created_at DESC
            """)
            
            rows = cur.fetchall()
            categories = []
            for row in rows:
                category = {
                    "id": row[0],
                    "name": row[1],
                    "created_at": row[2]
                }
                categories.append(category)
            return categories
        except Exception as e:
            raise e
