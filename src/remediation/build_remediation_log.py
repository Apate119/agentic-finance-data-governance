from pathlib import Path
from datetime import datetime

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENRICHED_RESULTS_PATH = PROJECT_ROOT / "outputs" / "scorecards" / "dq_results_enriched.csv"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "remediation"
REMEDIATION_LOG_PATH = OUTPUT_DIR / "remediation_action_log.csv"


def assign_priority(severity: str, failed_count: int) -> str:
    """
    Assigns remediation priority based on severity and number of failed records.
    """

    if severity == "High":
        return "P1"
    elif severity == "Medium" and failed_count >= 100:
        return "P2"
    elif severity == "Medium":
        return "P3"
    else:
        return "P4"


def recommend_action(check_name: str) -> str:
    """
    Provides business-friendly remediation guidance based on the failed control.
    """

    action_mapping = {
        "Customer name must not be null": "Review source customer records and populate missing customer_name values.",
        "Customer country must be valid": "Validate country values against approved reference data and update invalid records.",
        "Every account must map to a valid customer": "Investigate orphan account records and link them to valid customer identifiers.",
        "Account status must be valid": "Standardize account_status values against the approved status reference list.",
        "Every transaction must map to a valid account": "Investigate orphan transaction records and link them to valid account identifiers.",
        "Regulatory reported balance must not be null": "Review regulatory balance source feed and populate missing reported_balance values.",
    }

    return action_mapping.get(
        check_name,
        "Review failed records and remediate according to the control definition.",
    )


def build_remediation_log() -> pd.DataFrame:
    """
    Builds a remediation action log for failed DQ controls.
    """

    if not ENRICHED_RESULTS_PATH.exists():
        raise FileNotFoundError(
            f"Enriched DQ results not found at {ENRICHED_RESULTS_PATH}. "
            "Run src/reporting/build_governance_scorecard.py first."
        )

    enriched_results = pd.read_csv(ENRICHED_RESULTS_PATH)

    failed_controls = enriched_results[enriched_results["status"] == "FAIL"].copy()

    remediation_log = failed_controls[
        [
            "control_id",
            "check_name",
            "table_name",
            "dimension",
            "severity",
            "failed_count",
            "owner",
            "regulatory_relevance",
        ]
    ].copy()

    remediation_log["priority"] = remediation_log.apply(
        lambda row: assign_priority(
            severity=row["severity"],
            failed_count=row["failed_count"],
        ),
        axis=1,
    )

    remediation_log["remediation_status"] = "Open"

    remediation_log["recommended_action"] = remediation_log["check_name"].apply(
        recommend_action
    )

    remediation_log["created_timestamp"] = datetime.now().isoformat(timespec="seconds")
    remediation_log["target_resolution_days"] = remediation_log["priority"].map(
        {
            "P1": 2,
            "P2": 5,
            "P3": 10,
            "P4": 15,
        }
    )

    remediation_log = remediation_log[
        [
            "control_id",
            "check_name",
            "table_name",
            "dimension",
            "severity",
            "priority",
            "failed_count",
            "owner",
            "regulatory_relevance",
            "remediation_status",
            "target_resolution_days",
            "recommended_action",
            "created_timestamp",
        ]
    ]

    remediation_log = remediation_log.sort_values(
        by=["priority", "failed_count"],
        ascending=[True, False],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    remediation_log.to_csv(REMEDIATION_LOG_PATH, index=False)

    return remediation_log


if __name__ == "__main__":
    remediation_df = build_remediation_log()

    print("Remediation Action Log:\n")
    print(remediation_df.to_string(index=False))

    print(f"\nSaved remediation action log to: {REMEDIATION_LOG_PATH}")