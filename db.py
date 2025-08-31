import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

class Database:
    def __init__(self, db_url=None):
        self.db_url = db_url or os.environ.get("DATABASE_URL")
        self.init_db()

    def get_connection(self):
        return psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)

    def init_db(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS photos (
                file_id TEXT PRIMARY KEY,
                caption TEXT,
                username TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

    def add_photo(self, file_id: str, caption: str, username: str) -> None:
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO photos (file_id, caption, username, date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (file_id) DO UPDATE 
            SET caption = EXCLUDED.caption, username = EXCLUDED.username, date = EXCLUDED.date
        """, (file_id, caption, username, datetime.now()))
        conn.commit()
        cur.close()
        conn.close()

    def delete_photo(self, file_id: str) -> None:
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM photos WHERE file_id = %s", (file_id,))
        conn.commit()
        cur.close()
        conn.close()

    def get_photos(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM photos ORDER BY date DESC")
        photos = cur.fetchall()
        cur.close()
        conn.close()
        return photos

    def photo_exists(self, file_id: str) -> bool:
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM photos WHERE file_id = %s LIMIT 1", (file_id,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists
