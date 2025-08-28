from __future__ import annotations

from sqlalchemy import text

from .db_connector import DatabaseConnector


class PostgresConnector(DatabaseConnector):
    """Connector for PostgreSQL using psycopg2/psycopg dialect via SQLAlchemy."""

    def test_connection(self) -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False


