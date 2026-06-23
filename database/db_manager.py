"""
Central database management using SQLite.
"""
import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    _connection = None
    
    @classmethod
    def initialize(cls, db_path):
        cls._connection = sqlite3.connect(db_path, check_same_thread=False)
        cls._create_tables()
    
    @classmethod
    def _create_tables(cls):
        cur = cls._connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT UNIQUE,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                title TEXT,
                visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS speed_dial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                position INTEGER DEFAULT 0
            )
        """)
        cls._connection.commit()
    
    @classmethod
    def add_bookmark(cls, title, url):
        try:
            cur = cls._connection.cursor()
            cur.execute("INSERT OR IGNORE INTO bookmarks (title, url) VALUES (?, ?)", (title, url))
            cls._connection.commit()
        except Exception as e:
            print(f"Bookmark error: {e}")
    
    @classmethod
    def remove_bookmark(cls, url):
        cur = cls._connection.cursor()
        cur.execute("DELETE FROM bookmarks WHERE url=?", (url,))
        cls._connection.commit()
    
    @classmethod
    def is_bookmarked(cls, url):
        cur = cls._connection.cursor()
        cur.execute("SELECT COUNT(*) FROM bookmarks WHERE url=?", (url,))
        return cur.fetchone()[0] > 0
    
    @classmethod
    def get_all_bookmarks(cls):
        cur = cls._connection.cursor()
        cur.execute("SELECT title, url FROM bookmarks ORDER BY added_at DESC")
        return cur.fetchall()
    
    @classmethod
    def add_history(cls, url, title):
        try:
            cur = cls._connection.cursor()
            cur.execute("INSERT INTO history (url, title) VALUES (?, ?)", (url, title))
            cls._connection.commit()
        except Exception as e:
            print(f"History error: {e}")
    
    @classmethod
    def get_recent_history(cls, limit=100):
        cur = cls._connection.cursor()
        cur.execute("SELECT url, title FROM history ORDER BY visited_at DESC LIMIT ?", (limit,))
        return cur.fetchall()
    
    @classmethod
    def search_history(cls, keyword):
        cur = cls._connection.cursor()
        cur.execute("SELECT url, title FROM history WHERE title LIKE ? OR url LIKE ? ORDER BY visited_at DESC LIMIT 50",
                    (f"%{keyword}%", f"%{keyword}%"))
        return cur.fetchall()
    
    @classmethod
    def clear_history(cls):
        cur = cls._connection.cursor()
        cur.execute("DELETE FROM history")
        cls._connection.commit()
    
    @classmethod
    def set_setting(cls, key, value):
        cur = cls._connection.cursor()
        cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        cls._connection.commit()
    
    @classmethod
    def get_setting(cls, key, default=None):
        cur = cls._connection.cursor()
        cur.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else default