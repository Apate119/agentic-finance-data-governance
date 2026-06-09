from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "warehouse" / "finance_governance.duckdb"


TABLES = [
    "stg_customers",
    "stg_accounts",
    "stg_transactions",
    "stg_regulatory_balances",
]


def validate_tables() -> None:
    """
    Confirms that expected staging tables exist and prints row counts.
    """

    if not WAREHOUSE_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB warehouse not found at {WAREHOUSE_PATH}. "
            "Run load_to_duckdb.py first."
        )

    with duckdb.connect(str(WAREHOUSE_PATH)) as conn:
        print("DuckDB staging table row counts:\n")

        for table in TABLES:
            row_count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {row_count:,} rows")


if __name__ == "__main__":
    validate_tables()