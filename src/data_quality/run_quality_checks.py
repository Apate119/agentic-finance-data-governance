from pathlib import Path
from datetime import datetime

import duckdb
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "warehouse" / "finance_governance.duckdb"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "data_quality"
OUTPUT_PATH = OUTPUT_DIR / "quality_check_results.csv"


def run_check(
    conn: duckdb.DuckDBPyConnection,
    control_id: str,
    check_name: str,
    table_name: str,
    dimension: str,
    severity: str,
    sql: str,
) -> dict:
    """
    Runs a single data quality check.

    The SQL should return a single numeric value:
    - 0 means pass
    - anything above 0 means fail count
    """

    failed_count = conn.execute(sql).fetchone()[0]
    status = "PASS" if failed_count == 0 else "FAIL"

    return {
        "run_timestamp": datetime.now().isoformat(timespec="seconds"),
        "control_id": control_id,
        "check_name": check_name,
        "table_name": table_name,
        "dimension": dimension,
        "severity": severity,
        "failed_count": failed_count,
        "status": status,
    }


def run_quality_checks() -> pd.DataFrame:
    """
    Runs data quality checks across staging tables and writes results to CSV.
    """

    if not WAREHOUSE_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB warehouse not found at {WAREHOUSE_PATH}. "
            "Run src/ingestion/load_to_duckdb.py first."
        )

    checks = []

    with duckdb.connect(str(WAREHOUSE_PATH)) as conn:
        # Customer checks
        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-001",
                check_name="Customer ID must not be null",
                table_name="stg_customers",
                dimension="Completeness",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_customers
                    WHERE customer_id IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-002",
                check_name="Customer name must not be null",
                table_name="stg_customers",
                dimension="Completeness",
                severity="Medium",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_customers
                    WHERE customer_name IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-003",
                check_name="Customer created date must not be null",
                table_name="stg_customers",
                dimension="Completeness",
                severity="Medium",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_customers
                    WHERE created_date IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-004",
                check_name="Customer country must be valid",
                table_name="stg_customers",
                dimension="Validity",
                severity="Medium",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_customers
                    WHERE country NOT IN ('US', 'CA', 'UK', 'IN')
                       OR country IS NULL
                """,
            )
        )

        # Account checks
        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-005",
                check_name="Account ID must not be null",
                table_name="stg_accounts",
                dimension="Completeness",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_accounts
                    WHERE account_id IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-006",
                check_name="Every account must map to a valid customer",
                table_name="stg_accounts",
                dimension="Integrity",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_accounts a
                    LEFT JOIN stg_customers c
                        ON a.customer_id = c.customer_id
                    WHERE c.customer_id IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-007",
                check_name="Account status must be valid",
                table_name="stg_accounts",
                dimension="Validity",
                severity="Medium",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_accounts
                    WHERE account_status NOT IN ('Open', 'Closed', 'Suspended')
                       OR account_status IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-008",
                check_name="Account open date must not be null",
                table_name="stg_accounts",
                dimension="Completeness",
                severity="Medium",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_accounts
                    WHERE open_date IS NULL
                """,
            )
        )

        # Transaction checks
        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-009",
                check_name="Transaction ID must not be null",
                table_name="stg_transactions",
                dimension="Completeness",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_transactions
                    WHERE transaction_id IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-010",
                check_name="Every transaction must map to a valid account",
                table_name="stg_transactions",
                dimension="Integrity",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_transactions t
                    LEFT JOIN stg_accounts a
                        ON t.account_id = a.account_id
                    WHERE a.account_id IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-011",
                check_name="Transaction amount should not be zero",
                table_name="stg_transactions",
                dimension="Validity",
                severity="Medium",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_transactions
                    WHERE amount = 0
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-012",
                check_name="Transaction currency must be valid",
                table_name="stg_transactions",
                dimension="Validity",
                severity="Medium",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_transactions
                    WHERE currency NOT IN ('USD', 'CAD', 'GBP', 'INR')
                       OR currency IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-013",
                check_name="Transaction date must not be null",
                table_name="stg_transactions",
                dimension="Completeness",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_transactions
                    WHERE transaction_date IS NULL
                """,
            )
        )

        # Regulatory balance checks
        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-014",
                check_name="Regulatory reported balance must not be null",
                table_name="stg_regulatory_balances",
                dimension="Completeness",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_regulatory_balances
                    WHERE reported_balance IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-015",
                check_name="Regulatory reported balance should not be negative",
                table_name="stg_regulatory_balances",
                dimension="Validity",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_regulatory_balances
                    WHERE reported_balance < 0
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-016",
                check_name="Report date must not be null",
                table_name="stg_regulatory_balances",
                dimension="Completeness",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_regulatory_balances
                    WHERE report_date IS NULL
                """,
            )
        )

        checks.append(
            run_check(
                conn=conn,
                control_id="CTRL-017",
                check_name="Report name must not be null",
                table_name="stg_regulatory_balances",
                dimension="Completeness",
                severity="High",
                sql="""
                    SELECT COUNT(*)
                    FROM stg_regulatory_balances
                    WHERE report_name IS NULL
                """,
            )
        )

    results = pd.DataFrame(checks)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_PATH, index=False)

    return results


if __name__ == "__main__":
    dq_results = run_quality_checks()

    print("Data quality check results:\n")
    print(dq_results.to_string(index=False))
    print(f"\nSaved results to: {OUTPUT_PATH}")