from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DQ_RESULTS_PATH = PROJECT_ROOT / "outputs" / "data_quality" / "quality_check_results.csv"
CONTROL_INVENTORY_PATH = PROJECT_ROOT / "config" / "control_inventory.csv"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "scorecards"
SCORECARD_PATH = OUTPUT_DIR / "governance_scorecard.csv"
EXCEPTION_SUMMARY_PATH = OUTPUT_DIR / "dq_exception_summary.csv"
ENRICHED_RESULTS_PATH = OUTPUT_DIR / "dq_results_enriched.csv"


def calculate_readiness_status(pass_rate: float, high_severity_failures: int) -> str:
    """
    Converts DQ results into a regulatory readiness status.

    Simple rule:
    - Ready: pass rate >= 95% and no high-severity failures
    - Needs Review: pass rate >= 80% and no high-severity failures
    - Not Ready: anything else
    """

    if pass_rate >= 0.95 and high_severity_failures == 0:
        return "Ready"
    elif pass_rate >= 0.80 and high_severity_failures == 0:
        return "Needs Review"
    else:
        return "Not Ready"


def build_scorecard() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Builds:
    1. A governance scorecard summary
    2. A DQ exception summary grouped by control metadata
    3. An enriched DQ results file joined to the control inventory
    """

    if not DQ_RESULTS_PATH.exists():
        raise FileNotFoundError(
            f"DQ results not found at {DQ_RESULTS_PATH}. "
            "Run src/data_quality/run_quality_checks.py first."
        )

    if not CONTROL_INVENTORY_PATH.exists():
        raise FileNotFoundError(
            f"Control inventory not found at {CONTROL_INVENTORY_PATH}. "
            "Create config/control_inventory.csv first."
        )

    dq_results = pd.read_csv(DQ_RESULTS_PATH)
    control_inventory = pd.read_csv(CONTROL_INVENTORY_PATH)

    enriched_results = dq_results.merge(
        control_inventory[
            [
                "control_id",
                "control_description",
                "owner",
                "regulatory_relevance",
            ]
        ],
        on="control_id",
        how="left",
    )

    missing_metadata_count = enriched_results["owner"].isna().sum()

    total_checks = len(enriched_results)
    passed_checks = (enriched_results["status"] == "PASS").sum()
    failed_checks = (enriched_results["status"] == "FAIL").sum()

    pass_rate = passed_checks / total_checks if total_checks > 0 else 0

    high_severity_failures = len(
        enriched_results[
            (enriched_results["status"] == "FAIL")
            & (enriched_results["severity"] == "High")
        ]
    )

    medium_severity_failures = len(
        enriched_results[
            (enriched_results["status"] == "FAIL")
            & (enriched_results["severity"] == "Medium")
        ]
    )

    total_failed_records = enriched_results["failed_count"].sum()

    readiness_status = calculate_readiness_status(
        pass_rate=pass_rate,
        high_severity_failures=high_severity_failures,
    )

    scorecard = pd.DataFrame(
        [
            {
                "total_checks": total_checks,
                "passed_checks": passed_checks,
                "failed_checks": failed_checks,
                "pass_rate": round(pass_rate, 4),
                "pass_rate_pct": round(pass_rate * 100, 2),
                "high_severity_failures": high_severity_failures,
                "medium_severity_failures": medium_severity_failures,
                "total_failed_records": int(total_failed_records),
                "missing_control_metadata_count": int(missing_metadata_count),
                "regulatory_readiness_status": readiness_status,
            }
        ]
    )

    failed_results = enriched_results[enriched_results["status"] == "FAIL"].copy()

    exception_summary = (
        failed_results.groupby(
            [
                "control_id",
                "check_name",
                "table_name",
                "dimension",
                "severity",
                "owner",
                "regulatory_relevance",
            ],
            as_index=False,
        )
        .agg(
            failed_records=("failed_count", "sum"),
            failed_runs=("status", "count"),
        )
        .sort_values(
            by=["severity", "failed_records"],
            ascending=[True, False],
        )
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    scorecard.to_csv(SCORECARD_PATH, index=False)
    exception_summary.to_csv(EXCEPTION_SUMMARY_PATH, index=False)
    enriched_results.to_csv(ENRICHED_RESULTS_PATH, index=False)

    return scorecard, exception_summary, enriched_results


if __name__ == "__main__":
    scorecard_df, exception_summary_df, enriched_results_df = build_scorecard()

    print("Governance Scorecard:\n")
    print(scorecard_df.to_string(index=False))

    print("\nDQ Exception Summary:\n")
    print(exception_summary_df.to_string(index=False))

    print(f"\nSaved scorecard to: {SCORECARD_PATH}")
    print(f"Saved exception summary to: {EXCEPTION_SUMMARY_PATH}")
    print(f"Saved enriched DQ results to: {ENRICHED_RESULTS_PATH}")