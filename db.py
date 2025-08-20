import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS photos (
                    file_id TEXT PRIMARY KEY,
                    caption TEXT,
                    username TEXT,
                    date TEXT
                )
                """
            )
            db.commit()

    def add_photo(self, file_id: str, caption: str, username: str) -> None:
        with sqlite3.connect(self.db_path) as db:
            db.execute(
                "INSERT OR REPLACE INTO photos (file_id, caption, username, date) VALUES (?, ?, ?, ?)",
                (file_id, caption, username, datetime.now().isoformat()),
            )
            db.commit()

    def delete_photo(self, file_id: str) -> None:
        with sqlite3.connect(self.db_path) as db:
            db.execute("DELETE FROM photos WHERE file_id = ?", (file_id,))
            db.commit()

    def get_photos(self):
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            cursor = db.execute("SELECT * FROM photos ORDER BY date DESC")
            return [dict(row) for row in cursor.fetchall()]

    def photo_exists(self, file_id: str) -> bool:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.execute(
                "SELECT 1 FROM photos WHERE file_id = ? LIMIT 1", (file_id,)
            )
            return cursor.fetchone() is not None
