from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
WAREHOUSE_DIR = PROJECT_ROOT / "data" / "warehouse"
WAREHOUSE_PATH = WAREHOUSE_DIR / "finance_governance.duckdb"


TABLES = {
    "customers": "customers.csv",
    "accounts": "accounts.csv",
    "transactions": "transactions.csv",
    "regulatory_balances": "regulatory_balances.csv",
}


def load_csv_to_duckdb() -> None:
    """
    Loads raw CSV files into DuckDB staging tables.

    This is intentionally simple for now:
    - CSV files are the source layer
    - DuckDB is the local warehouse
    - Each CSV becomes a staging table prefixed with stg_
    """

    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(WAREHOUSE_PATH)) as conn:
        for table_name, file_name in TABLES.items():
            csv_path = RAW_DATA_DIR / file_name
            staging_table = f"stg_{table_name}"

            if not csv_path.exists():
                raise FileNotFoundError(f"Missing expected file: {csv_path}")

            print(f"Loading {csv_path.name} into {staging_table}...")

            conn.execute(
                f"""
                CREATE OR REPLACE TABLE {staging_table} AS
                SELECT *
                FROM read_csv_auto('{csv_path}');
                """
            )

        print(f"\nLoaded {len(TABLES)} tables into DuckDB.")
        print(f"Warehouse path: {WAREHOUSE_PATH}")


if __name__ == "__main__":
    load_csv_to_duckdb()