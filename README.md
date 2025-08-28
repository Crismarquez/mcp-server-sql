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


Claude Desktop (conexión local)

1. Construye la imagen de Docker (una sola vez):
```bash
docker build -t sales-mcp .
```

2. En Windows, crea/edita el archivo de configuración de Claude Desktop en:
`%APPDATA%\Claude\claude_desktop_config.json`

3. Agrega esta configuración para ejecutar el MCP dentro de Docker:
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

4. Guarda el archivo y reinicia Claude Desktop.

Nota: si quieres usar otro conector distinto a `mock`, ajusta la variable `DB_TYPE` y, de ser necesario, agrega `-e DB_CONN_STR=...` siguiendo la sección "Environment" de este README.

