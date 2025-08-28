from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Dict, Iterable, Optional

import sqlalchemy
from sqlalchemy.engine import Engine, Connection, Result


class DatabaseConnector(ABC):
    """Abstract base class for database connectors.

    Provides a common interface for establishing connections and executing queries
    using SQLAlchemy engines, along with small convenience helpers.
    """

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine: Optional[Engine] = None

    def connect(self) -> None:
        """Initialize SQLAlchemy engine lazily."""
        if self.engine is None:
            self.engine = sqlalchemy.create_engine(self.connection_string)

    def get_connection(self) -> Connection:
        """Get a connection from the SQLAlchemy engine."""
        if self.engine is None:
            self.connect()
        assert self.engine is not None
        return self.engine.connect()

    @contextmanager
    def connection(self) -> Iterable[Connection]:
        conn = self.get_connection()
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Result:
        """Execute a SQL statement and return a Result.

        For simple use-cases; callers can use connection() for more control.
        """
        with self.connection() as conn:
            return conn.execute(sqlalchemy.text(sql), params or {})

    @abstractmethod
    def test_connection(self) -> bool:
        """Test DB connectivity; implementations should return True/False."""
        raise NotImplementedError


