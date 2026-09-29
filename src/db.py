import sqlite3
import asyncio

def get_connection():
    conn = sqlite3.connect('podcast.db')
    conn.row_factory = sqlite3.Row
    return conn

def db_init():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                audio_url TEXT NOT NULL,
                duration INTEGER,
                size INTEGER,
                pub_date TEXT
            )
        ''')


def add_episode(title, descripiton, audio_url, duration, size, pub_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO episodes(title, description, audio_url, duration, size, pub_date)
            VALUES (?, ?, ?, ?, ?)
        ''',
        (title, descripiton, audio_url, duration, size, pub_date)
        )


def get_all_episodes():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, description, audio_url, duration, size, pub_date FROM episodes')
        return cursor.fetchall()