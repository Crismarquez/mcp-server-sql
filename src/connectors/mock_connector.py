from __future__ import annotations

from typing import Any, List, Tuple

import pandas as pd

from .db_connector import DatabaseConnector


class MockConnector(DatabaseConnector):
    """Mock connector with in-memory data for offline testing, backed by pandas."""

    def __init__(self, connection_string: str = "mock://memory"):
        super().__init__(connection_string)
        # sale_date, region, seller_name, product_name, sales_amount
        data: List[Tuple[str, str, str, str, float]] = [
            ("2025-01-01", "North", "Alice", "Widget", 1200.0),
            ("2025-01-01", "North", "Bob", "Gizmo", 800.0),
            ("2025-01-01", "South", "Carlos", "Widget", 400.0),
            ("2025-01-02", "South", "Carlos", "Widget", 1500.0),
            ("2025-01-02", "North", "Alice", "Gadget", 700.0),
            ("2025-01-02", "West", "Diana", "Gizmo", 300.0),
            ("2025-01-03", "West", "Diana", "Widget", 900.0),
            ("2025-01-03", "South", "Carlos", "Gadget", 600.0),
            ("2025-01-03", "North", "Bob", "Widget", 500.0),
            ("2025-01-03", "North", "Alice", "Widget", 200.0),
        ]
        self.df = pd.DataFrame(
            data,
            columns=[
                "sale_date",
                "region",
                "seller_name",
                "product_name",
                "sales_amount",
            ],
        )

    def connect(self) -> None:
        # No real engine; ignore.
        return None

    def get_connection(self):
        # Return self as a minimal connection-like object
        return self

    # Context manager methods to mimic connection usage
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    class _Rows:
        def __init__(self, rows: List[Tuple[Any, ...]]):
            self._rows = rows

        def fetchall(self):
            return list(self._rows)

        def fetchone(self):
            return self._rows[0] if self._rows else None

    # Minimal execute emulation for our limited queries used by tools
    def execute(self, query: Any, params: Any = None):
        # Accept raw SQL string or SQLAlchemy TextClause
        sql = str(query)
        q = " ".join(sql.lower().split())
        params = params or {}
        if "from sales" not in q:
            return self._Rows([])

        if "group by seller_name" in q and "where region" in q:
            # best_sellers_by_region(region)
            region = params.get("region")
            if not region:
                return self._Rows([])
            filtered = self.df[self.df["region"].str.lower() == str(region).lower()]
            if filtered.empty:
                return self._Rows([])
            agg = (
                filtered.groupby("seller_name")["sales_amount"].sum().sort_values(ascending=False)
            )
            rows = [(name, float(total)) for name, total in agg.items()]
            return self._Rows(rows)

        if "group by product_name" in q:
            # top_products()
            agg = self.df.groupby("product_name")["sales_amount"].sum().sort_values(ascending=False)
            rows = [(name, float(total)) for name, total in agg.items()]
            return self._Rows(rows)

        if "sum(sales_amount) as total_sales" in q and "cast(sale_date as date)" in q and "where" in q:
            # sales_by_date(date)
            date = params.get("date")
            if not date:
                return self._Rows([(0.0,)])
            total = float(self.df.loc[self.df["sale_date"] == str(date), "sales_amount"].sum())
            return self._Rows([(total,)])

        return self._Rows([])

    def test_connection(self) -> bool:
        return True


