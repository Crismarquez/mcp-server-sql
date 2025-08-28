Sales Analytics MCP Server

Tools for querying sales data via Model Context Protocol with pluggable database connectors (Databricks, PostgreSQL, Azure SQL, or Mock).

Setup

1. Create and activate a virtualenv (optional)
2. Install deps:
```bash
pip install -r requirements.txt
```
3. Copy env template and configure:
```bash
copy .env.example .env
```

Environment

- DB_TYPE: one of databricks, postgres, azure, mock (default: mock)
- DB_CONN_STR: SQLAlchemy connection string for selected DB (not needed for mock)

Connection string examples

- Databricks: databricks+connector://token:<TOKEN>@<workspace-host>/<catalog>.<schema>
- PostgreSQL: postgresql+psycopg2://user:password@host:5432/dbname
- Azure SQL: mssql+pyodbc://USER:PASSWORD@SERVER.database.windows.net:1433/DB?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no

Run

```bash
python main.py
```

Docker

```bash
docker build -t sales-mcp .
docker run --rm -e DB_TYPE=mock sales-mcp
```

Tools

- best_sellers_by_region(region: str)
- top_products(limit: int = 5)
- sales_by_date(date: str)


Claude Desktop (local connection)

1. Build the Docker image (once):
```bash
docker build -t sales-mcp .
```

2. On Windows, create/edit the Claude Desktop config file at:
`%APPDATA%\Claude\claude_desktop_config.json`

3. Add this configuration to run the MCP inside Docker:
```json
{
    "mcpServers": {
        "sales-analytics": {
            "command": "docker",
            "args": [
                "run", "--rm", "-i",
                "-e", "DB_TYPE=mock",
                "sales-mcp"
            ]
        }
    }
}
```

4. Save the file and restart Claude Desktop.

Note: If you want to use a connector other than `mock`, set `DB_TYPE` accordingly and, if needed, add `-e DB_CONN_STR=...` following the "Environment" section of this README.

