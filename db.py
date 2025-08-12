import sqlite3


class Database:
    def __init__(self):
        self.db_path = "database.db"
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS tracks (
                    track_id TEXT PRIMARY KEY,
                    title VARCHAR(255),
                    performer VARCHAR(255),
                    duration INT
                )
            """
            )
            db.commit()

    def add_track(self, track_id: str, title: str, performer: str, duration: int):
        with sqlite3.connect(self.db_path) as db:
            db.execute(
                "INSERT OR REPLACE INTO tracks (track_id, title, performer, duration) VALUES (?, ?, ?, ?)",
                (track_id, title, performer, duration),
            )
            db.commit()

    def delete_track(self, track_id: str):
        with sqlite3.connect(self.db_path) as db:
            db.execute("DELETE FROM tracks WHERE track_id = ?", (track_id,))
            db.commit()

    def get_tracks(self):
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            cursor = db.execute("SELECT * FROM tracks")
            return [dict(row) for row in cursor.fetchall()]
