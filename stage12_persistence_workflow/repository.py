import sqlite3
from datetime import datetime
from typing import List, Optional


class RunRepository:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._init_table()

    def _init_table(self) -> None:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS stage12_runs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_query TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )
                conn.commit()
        except Exception:
            return

    def save(self, user_query: str, answer: str) -> Optional[int]:
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO stage12_runs (user_query, answer, created_at) VALUES (?, ?, ?)",
                    (user_query, answer, datetime.utcnow().isoformat()),
                )
                conn.commit()
                return int(cursor.lastrowid)
        except Exception:
            return None

    def list_recent(self, limit: int) -> List[dict]:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT id, user_query, created_at FROM stage12_runs ORDER BY id DESC LIMIT ?",
                    (limit,),
                ).fetchall()
                return [dict(row) for row in rows]
        except Exception:
            return []
