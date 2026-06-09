# Executive Summary

## Overview

The Agentic Finance Data Governance Pipeline is a portfolio project that simulates how financial institutions can monitor, score, and remediate data quality issues across regulatory reporting datasets.

The project uses synthetically generated finance data to demonstrate a practical governance workflow covering ingestion, validation, control execution, scorecard reporting, exception management, and remediation tracking.

## Business Problem

Financial institutions depend on accurate, complete, and traceable data for regulatory reporting. Poor data quality can create downstream reporting errors, manual reconciliation work, delayed submissions, and increased regulatory risk.

Common challenges include:

* Missing customer or account reference data
* Invalid account statuses, countries, or transaction values
* Broken relationships between customers, accounts, and transactions
* Incomplete regulatory balance records
* Limited visibility into control ownership and remediation status

## Solution

This project implements a modular data governance pipeline that:

1. Generates synthetic customer, account, transaction, and regulatory balance datasets
2. Loads source data into a local DuckDB warehouse
3. Validates staging table loads
4. Runs automated data quality checks across completeness, validity, and integrity dimensions
5. Enriches control results with governance metadata from a control inventory
6. Produces executive-style governance scorecards
7. Exports exception-level failed records
8. Creates a remediation action log with owners, priorities, target resolution timelines, and recommended actions

## Key Results From Sample Run

One sample pipeline execution produced the following governance outcome:

| Metric | Value |
| --- | ---: |
| Total Controls | 17 |
| Passed Controls | 11 |
| Failed Controls | 6 |
| Pass Rate | 64.71% |
| Failed Records | 347 |
| High Severity Failures | 3 |
| Medium Severity Failures | 3 |
| Regulatory Readiness Status | Not Ready |

The dataset was classified as **Not Ready** due to high-severity completeness and integrity failures.

## Example Issues Identified

The pipeline identified several data quality issues that would be meaningful in a regulatory reporting context:

| Issue Type | Example |
| --- | --- |
| Completeness | Missing customer names and regulatory reported balances |
| Validity | Invalid customer countries and account statuses |
| Integrity | Accounts not mapped to valid customers and transactions not mapped to valid accounts |

## Governance Value

This project demonstrates how technical data quality checks can be connected to governance operating model concepts, including:

* Control IDs
* Data quality dimensions
* Control severity
* Assigned data owners
* Regulatory relevance
* Executive scorecards
* Exception exports
* Remediation prioritization
* Target resolution timelines

This structure mirrors how finance data governance teams manage reporting readiness and issue remediation in regulated environments.

## Technical Implementation

The current implementation runs locally using:

* Python
* pandas
* DuckDB
* Faker
* CSV-based inputs and outputs

The pipeline is orchestrated through a single runner script:

    python src/pipeline/run_pipeline.py

## Current Outputs

The project produces the following primary outputs:

| Output | Purpose |
| --- | --- |
| `outputs/data_quality/quality_check_results.csv` | Control-level data quality results |
| `outputs/scorecards/governance_scorecard.csv` | Executive governance scorecard |
| `outputs/scorecards/dq_results_enriched.csv` | Data quality results enriched with control metadata |
| `outputs/scorecards/dq_exception_summary.csv` | Failed controls summarized by metadata |
| `outputs/exceptions/*.csv` | Exception-level failed records |
| `outputs/exceptions/exception_export_summary.csv` | Summary of exception files exported |
| `outputs/remediation/remediation_action_log.csv` | Owner-assigned remediation action log |

## Future Scalability

The project is intentionally modular so it can later be extended into a more enterprise-grade architecture.

| Current Component | Future-State Extension |
| --- | --- |
| CSV source files | Cloud storage or enterprise source systems |
| DuckDB warehouse | Snowflake or Databricks |
| Python transformation scripts | dbt or Databricks workflows |
| Local pipeline runner | Airflow, Dagster, or cloud-native orchestration |
| CSV scorecards | BI dashboards or governance reporting portals |
| Static remediation log | Workflow-based issue management or LLM-assisted remediation recommendations |

## Summary

This project demonstrates practical experience across data governance, regulatory reporting readiness, data quality control design, exception management, remediation workflow design, and Python-based data automation.

It is designed to be lightweight enough to run locally while still reflecting patterns used in enterprise finance data governance environments.