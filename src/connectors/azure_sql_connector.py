from __future__ import annotations

from sqlalchemy import text

from .db_connector import DatabaseConnector


class AzureSqlConnector(DatabaseConnector):
    """Connector for Azure SQL (SQL Server) via ODBC/pyodbc dialect.

    Example connection string (ODBC Driver 18):
    mssql+pyodbc://USER:PASSWORD@SERVER.database.windows.net:1433/DB?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no
    """

    def test_connection(self) -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False


