from __future__ import annotations

import os

from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

from src.connectors.databricks_connector import DatabricksConnector
from src.connectors.postgres_connector import PostgresConnector
from src.connectors.azure_sql_connector import AzureSqlConnector
from src.connectors.mock_connector import MockConnector
from src.services.sales_service import (
    get_best_sellers_by_region,
    get_top_products,
    get_sales_by_date,
)


# Load environment variables from .env if present
load_dotenv()


def _build_connector():
    db_type = (os.getenv("DB_TYPE") or "mock").lower()
    conn_str = os.getenv("DB_CONN_STR", "")

    if db_type == "databricks":
        if not conn_str:
            raise ValueError("DB_CONN_STR is required for Databricks")
        return DatabricksConnector(conn_str)
    if db_type in ("postgres", "postgresql"):
        if not conn_str:
            raise ValueError("DB_CONN_STR is required for PostgreSQL")
        return PostgresConnector(conn_str)
    if db_type in ("azure", "mssql", "sqlserver"):
        if not conn_str:
            raise ValueError("DB_CONN_STR is required for Azure SQL")
        return AzureSqlConnector(conn_str)
    if db_type == "mock":
        return MockConnector()

    raise ValueError(f"Unsupported DB_TYPE: {db_type}")


# Initialize MCP
mcp = FastMCP("sales-analytics")

# Initialize DB connector (selected by environment)
db = _build_connector()


@mcp.tool()
async def best_sellers_by_region(region: str) -> str:
    """Get top 5 sellers by region.

    Args:
        region: sales region name
    """
    try:
        rows = get_best_sellers_by_region(db, region)
        if not rows:
            return f"No sellers found in region {region}"
        top = rows[:5]
        return "\n".join([f"{r[0]}: {r[1]}" for r in top])
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def top_products(limit: int = 5) -> str:
    """Get top selling products."""
    try:
        rows = get_top_products(db)
        top = rows[: max(1, int(limit))]
        return "\n".join([f"{r[0]}: {r[1]}" for r in top])
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def sales_by_date(date: str) -> str:
    """Get total sales for a given date.

    Args:
        date: YYYY-MM-DD
    """
    try:
        result = get_sales_by_date(db, date)
        total = 0 if result is None or result[0] is None else result[0]
        return f"Total sales on {date}: {total}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")


