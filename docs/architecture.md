# Project Architecture

This project follows a modular finance data governance pipeline pattern designed to simulate how regulatory reporting datasets can be ingested, validated, scored, and routed for remediation.

## Architecture Flow

    Synthetic Source Data
    (customers, accounts, transactions, regulatory balances)
            ↓
    Raw CSV Landing Zone
    data/raw/
            ↓
    DuckDB Local Warehouse
    data/warehouse/finance_governance.duckdb
            ↓
    Staging Table Validation
    src/ingestion/validate_duckdb_load.py
            ↓
    Data Quality Control Execution
    src/data_quality/run_quality_checks.py
            ↓
    Control Metadata Enrichment
    config/control_inventory.csv
            ↓
    Governance Scorecards
    outputs/scorecards/
            ↓
    Exception-Level Exports
    outputs/exceptions/
            ↓
    Remediation Action Log
    outputs/remediation/remediation_action_log.csv

## Component Overview

| Layer | Purpose | Location |
| --- | --- | --- |
| Source Data Generation | Creates synthetic finance datasets for customers, accounts, transactions, and regulatory balances | `src/ingestion/generate_sample_data.py` |
| Raw Data Storage | Stores generated source CSV files | `data/raw/` |
| Local Warehouse | Loads source files into DuckDB staging tables | `data/warehouse/finance_governance.duckdb` |
| Load Validation | Confirms staging tables were created and populated successfully | `src/ingestion/validate_duckdb_load.py` |
| Data Quality Controls | Runs completeness, validity, and integrity checks | `src/data_quality/run_quality_checks.py` |
| Control Inventory | Stores governance metadata including owner, severity, and regulatory relevance | `config/control_inventory.csv` |
| Scorecard Reporting | Produces executive-style governance and regulatory readiness outputs | `outputs/scorecards/` |
| Exception Management | Exports failed records for remediation review | `outputs/exceptions/` |
| Remediation Workflow | Assigns failed controls to owners with priority and target resolution timelines | `outputs/remediation/` |

## Current Implementation

The current implementation runs locally using Python, pandas, DuckDB, and CSV-based inputs and outputs.

## Future-State Architecture

The project is designed so the local components can later be extended into an enterprise-grade architecture:

| Current Component | Future-State Extension |
| --- | --- |
| CSV source files | Cloud storage or enterprise source systems |
| DuckDB local warehouse | Snowflake or Databricks |
| Python transformation scripts | dbt models or Databricks workflows |
| Local pipeline runner | Airflow, Dagster, or cloud-native orchestration |
| CSV scorecards | BI dashboards or governance reporting portals |
| Static remediation log | Workflow-based issue management or LLM-assisted remediation recommendations |