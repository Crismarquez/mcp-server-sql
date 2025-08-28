from __future__ import annotations

from sqlalchemy import text

from src.connectors.db_connector import DatabaseConnector


def get_best_sellers_by_region(db: DatabaseConnector, region: str):
    query = text(
        """
        SELECT seller_name, SUM(sales_amount) AS total_sales
        FROM sales
        WHERE region = :region
        GROUP BY seller_name
        ORDER BY total_sales DESC
        """
    )
    with db.get_connection() as conn:
        return conn.execute(query, {"region": region}).fetchall()


def get_top_products(db: DatabaseConnector):
    query = text(
        """
        SELECT product_name, SUM(sales_amount) AS total_sales
        FROM sales
        GROUP BY product_name
        ORDER BY total_sales DESC
        """
    )
    with db.get_connection() as conn:
        return conn.execute(query).fetchall()


def get_sales_by_date(db: DatabaseConnector, date: str):
    query = text(
        """
        SELECT SUM(sales_amount) AS total_sales
        FROM sales
        WHERE CAST(sale_date AS DATE) = :date
        """
    )
    with db.get_connection() as conn:
        return conn.execute(query, {"date": date}).fetchone()


