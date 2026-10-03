"""
Database operations and Audit Logger for Enterprise Compliance Firewall.
Stored in core/database.py as per modular design guidelines.
"""

import sqlite3
import os
import json
import time
from typing import Dict, Any, List, Optional
from rlcd_jev.core.config import settings
from rlcd_jev.core.logger import logger


class AuditDatabase:
    """
    Manages SQLite database storage for firewall audit logs and decision telemetry.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.database_path
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp REAL,
                        status TEXT,
                        risk_level TEXT,
                        category TEXT,
                        confidence REAL,
                        latency_ms REAL,
                        prompt_hash TEXT,
                        details_json TEXT
                    )
                """)
                conn.commit()
                logger.debug(f"Audit database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database at {self.db_path}: {e}")

    def log_decision(
        self,
        status: str,
        risk_level: str,
        category: str,
        confidence: float,
        latency_ms: float,
        prompt: str,
        details: Dict[str, Any]
    ) -> bool:
        """Persists a firewall decision log entry into SQLite."""
        if not settings.enable_db_audit:
            return False

        try:
            prompt_hash = str(hash(prompt))
            details_json = json.dumps(details)
            timestamp = time.time()

            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO audit_logs 
                    (timestamp, status, risk_level, category, confidence, latency_ms, prompt_hash, details_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (timestamp, status, risk_level, category, confidence, latency_ms, prompt_hash, details_json))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to insert audit log entry: {e}")
            return False

    def get_recent_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves recent audit log entries."""
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to query audit logs: {e}")
            return []
