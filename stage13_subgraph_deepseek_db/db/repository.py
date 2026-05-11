import os
import sqlite3
from datetime import datetime
from typing import List, Optional


class LearningRunRepository:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._ensure_parent_dir()
        self._init_table()

    def _ensure_parent_dir(self) -> None:
        parent_dir = os.path.dirname(self._db_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

    def _init_table(self) -> None:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS learning_runs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_query TEXT NOT NULL,
                        intent TEXT NOT NULL,
                        plan TEXT NOT NULL,
                        final_answer TEXT NOT NULL,
                        quality_score INTEGER NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )
                conn.commit()
        except Exception:
            # 查询或建表失败时，不抛异常，保持流程继续
            return

    def save_run(
        self, user_query: str, intent: str, plan: str, final_answer: str, quality_score: int
    ) -> Optional[int]:
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO learning_runs
                    (user_query, intent, plan, final_answer, quality_score, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_query,
                        intent,
                        plan,
                        final_answer,
                        quality_score,
                        datetime.utcnow().isoformat(),
                    ),
                )
                conn.commit()
                return int(cursor.lastrowid)
        except Exception:
            # SQL 执行失败时，返回 None，不抛异常
            return None

    def list_recent(self, limit: int) -> List[dict]:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """
                    SELECT id, user_query, intent, quality_score, created_at
                    FROM learning_runs
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
                return [dict(row) for row in rows]
        except Exception:
            # SQL 查询失败时，返回空数组，不抛异常
            return []
