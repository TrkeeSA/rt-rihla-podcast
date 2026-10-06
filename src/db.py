import sqlite3
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = sqlite3.connect('podcast.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def db_init():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                description TEXT,
                audio_url TEXT NOT NULL UNIQUE,
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
            VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (title, descripiton, audio_url, duration, size, pub_date)
        )


def get_all_episodes():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, description, audio_url, duration, size, pub_date FROM episodes')
        return cursor.fetchall()


def check_episode_exists(audio_url):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT title, audio_url, pub_date FROM episodes WHERE audio_url = ?', (audio_url,))
        result = cursor.fetchone()
        if result:
            print(f"Episode already exists: {result['title']}, Date: {result['pub_date']}")
            return True
        return False


def last_episode():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT pub_date FROM episodes ORDER BY pub_date DESC LIMIT 1')
        result = cursor.fetchone()
        return result[0] if result else None


if __name__ == "__main__":
    db_init()
    print("Database initialized successfully.")