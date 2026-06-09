from pathlib import Path

import duckdb
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "warehouse" / "finance_governance.duckdb"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "exceptions"


EXCEPTION_QUERIES = {
    "customer_name_null_exceptions.csv": """
        SELECT
            'Customer name must not be null' AS check_name,
            'Completeness' AS dimension,
            'Medium' AS severity,
            *
        FROM stg_customers
        WHERE customer_name IS NULL
    """,

    "invalid_country_exceptions.csv": """
        SELECT
            'Customer country must be valid' AS check_name,
            'Validity' AS dimension,
            'Medium' AS severity,
            *
        FROM stg_customers
        WHERE country NOT IN ('US', 'CA', 'UK', 'IN')
           OR country IS NULL
    """,

    "orphan_account_exceptions.csv": """
        SELECT
            'Every account must map to a valid customer' AS check_name,
            'Integrity' AS dimension,
            'High' AS severity,
            a.*
        FROM stg_accounts a
        LEFT JOIN stg_customers c
            ON a.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """,

    "invalid_account_status_exceptions.csv": """
        SELECT
            'Account status must be valid' AS check_name,
            'Validity' AS dimension,
            'Medium' AS severity,
            *
        FROM stg_accounts
        WHERE account_status NOT IN ('Open', 'Closed', 'Suspended')
           OR account_status IS NULL
    """,

    "orphan_transaction_exceptions.csv": """
        SELECT
            'Every transaction must map to a valid account' AS check_name,
            'Integrity' AS dimension,
            'High' AS severity,
            t.*
        FROM stg_transactions t
        LEFT JOIN stg_accounts a
            ON t.account_id = a.account_id
        WHERE a.account_id IS NULL
    """,

    "null_regulatory_balance_exceptions.csv": """
        SELECT
            'Regulatory reported balance must not be null' AS check_name,
            'Completeness' AS dimension,
            'High' AS severity,
            *
        FROM stg_regulatory_balances
        WHERE reported_balance IS NULL
    """,
}


def export_exceptions() -> pd.DataFrame:
    """
    Exports exception-level records for failed data quality checks.
    """

    if not WAREHOUSE_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB warehouse not found at {WAREHOUSE_PATH}. "
            "Run src/ingestion/load_to_duckdb.py first."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_rows = []

    with duckdb.connect(str(WAREHOUSE_PATH)) as conn:
        for file_name, sql in EXCEPTION_QUERIES.items():
            output_path = OUTPUT_DIR / file_name

            exception_df = conn.execute(sql).fetchdf()
            exception_df.to_csv(output_path, index=False)

            summary_rows.append(
                {
                    "exception_file": file_name,
                    "record_count": len(exception_df),
                    "output_path": str(output_path),
                }
            )

            print(f"Exported {len(exception_df):,} records to {output_path}")

    summary_df = pd.DataFrame(summary_rows)
    summary_path = OUTPUT_DIR / "exception_export_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    print(f"\nSaved exception export summary to: {summary_path}")

    return summary_df


if __name__ == "__main__":
    export_summary = export_exceptions()

    print("\nException Export Summary:\n")
    print(export_summary.to_string(index=False))