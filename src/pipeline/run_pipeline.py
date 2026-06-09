from pathlib import Path
import subprocess
import sys
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]


PIPELINE_STEPS = [
    {
        "name": "Generate sample source data",
        "script": "src/ingestion/generate_sample_data.py",
    },
    {
        "name": "Load source data to DuckDB",
        "script": "src/ingestion/load_to_duckdb.py",
    },
    {
        "name": "Validate DuckDB staging tables",
        "script": "src/ingestion/validate_duckdb_load.py",
    },
    {
        "name": "Run data quality checks",
        "script": "src/data_quality/run_quality_checks.py",
    },
    {
        "name": "Build governance scorecard",
        "script": "src/reporting/build_governance_scorecard.py",
    },
    {
        "name": "Export DQ exceptions",
        "script": "src/exceptions/export_dq_exceptions.py",
    },
    {
    "name": "Build remediation action log",
    "script": "src/remediation/build_remediation_log.py",
    },
]


def run_step(step_name: str, script_path: str) -> None:
    """
    Runs one pipeline step as a Python subprocess.
    If the step fails, the pipeline stops immediately.
    """

    full_script_path = PROJECT_ROOT / script_path

    if not full_script_path.exists():
        raise FileNotFoundError(f"Pipeline step not found: {full_script_path}")

    print("\n" + "=" * 80)
    print(f"Starting step: {step_name}")
    print(f"Script: {script_path}")
    print("=" * 80)

    result = subprocess.run(
        [sys.executable, str(full_script_path)],
        cwd=PROJECT_ROOT,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at step: {step_name}")

    print(f"Completed step: {step_name}")


def run_pipeline() -> None:
    """
    Runs the full finance data governance pipeline end-to-end.
    """

    start_time = datetime.now()

    print("\nFinance Data Governance Pipeline")
    print(f"Started at: {start_time.isoformat(timespec='seconds')}")

    for step in PIPELINE_STEPS:
        run_step(
            step_name=step["name"],
            script_path=step["script"],
        )

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 80)
    print("Pipeline completed successfully")
    print(f"Finished at: {end_time.isoformat(timespec='seconds')}")
    print(f"Duration: {duration}")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()