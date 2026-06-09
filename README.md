# Agentic Finance Data Governance Pipeline

This project is an end-to-end finance data governance pipeline that simulates how banking data can be ingested, validated, scored, and routed for remediation in a regulatory reporting environment.

The pipeline generates synthetic customer, account, transaction, and regulatory balance data, loads it into a local DuckDB warehouse, runs automated data quality controls, produces a governance scorecard, exports exception-level records, and creates a remediation action log assigned to data owners.

All data used in this project is synthetically generated and does not contain confidential, customer, or production financial information.

## Project Objective

Financial institutions rely on accurate, complete, and traceable data for regulatory reporting. This project demonstrates a lightweight but scalable framework for monitoring data quality and regulatory readiness across critical finance datasets.

The design is intentionally modular so the local DuckDB implementation can later be extended to Snowflake, Databricks, dbt, Airflow, or cloud storage.

For a business-facing project summary, see [`docs/executive_summary.md`](docs/executive_summary.md).
For a more detailed architecture overview, see [`docs/architecture.md`](docs/architecture.md).
For a business view of the implemented controls, see [`docs/control_catalog.md`](docs/control_catalog.md).
For guidance on interpreting generated outputs, see [`docs/output_guide.md`](docs/output_guide.md).
For source dataset definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

## Pipeline Flow

```text
Synthetic source data
        ↓
DuckDB staging tables
        ↓
Data quality checks
        ↓
Governance scorecard
        ↓
Exception exports
        ↓
Remediation action log
```

## Key Features

* Generates synthetic finance and regulatory reporting datasets
* Loads source files into a local DuckDB warehouse
* Validates staging table row counts
* Executes automated data quality controls
* Evaluates completeness, validity, and integrity dimensions
* Maintains a governance control inventory with control IDs, owners, and regulatory relevance
* Produces an executive-style regulatory readiness scorecard
* Exports exception-level failed records for remediation
* Creates a remediation action log with assigned owners, priorities, target resolution timelines, and recommended actions
* Uses a modular structure that can later support Snowflake, Databricks, dbt, or workflow orchestration tools

## Data Domains

The project currently includes four source datasets:

| Dataset | Description |
| --- | --- |
| customers | Customer reference data containing customer identifiers, names, segments, countries, and creation dates |
| accounts | Account master data containing account identifiers, customer relationships, account types, statuses, and open dates |
| transactions | Transaction-level activity containing transaction identifiers, account relationships, dates, transaction types, amounts, and currencies |
| regulatory_balances | Regulatory reporting balance data containing report dates, account types, reported balances, and report names |

## Data Quality Dimensions

The pipeline evaluates controls across the following dimensions:

| Dimension | Purpose |
| --- | --- |
| Completeness | Confirms required fields are populated |
| Validity | Confirms values match expected formats, ranges, or approved reference values |
| Integrity | Confirms relationships between datasets are valid and traceable |

## Control Inventory

The project includes a control inventory located at `config/control_inventory.csv`.

The control inventory documents each data quality rule with business and governance metadata:

| Field | Description |
| --- | --- |
| control_id | Unique control identifier |
| control_name | Business-readable control name |
| table_name | Table where the control is applied |
| column_name | Primary field being evaluated |
| dimension | Data quality dimension |
| severity | Control severity |
| control_description | Description of what the control validates |
| owner | Assigned data owner |
| regulatory_relevance | Why the control matters for reporting or governance |

## Example Scorecard Results

One sample pipeline run produced:

| Metric | Value |
| --- | ---: |
| Total Controls | 17 |
| Passed Controls | 11 |
| Failed Controls | 6 |
| Pass Rate | 64.71% |
| Failed Records | 347 |
| High Severity Failures | 3 |
| Medium Severity Failures | 3 |
| Missing Control Metadata Records | 0 |
| Regulatory Readiness Status | Not Ready |

The dataset was classified as **Not Ready** because high-severity completeness and integrity failures were identified.

## Example Failed Controls

| Control ID | Failed Control | Severity | Owner | Failed Records |
| --- | --- | --- | --- | ---: |
| CTRL-006 | Every account must map to a valid customer | High | Account Data Owner | 1 |
| CTRL-010 | Every transaction must map to a valid account | High | Transaction Data Owner | 1 |
| CTRL-014 | Regulatory reported balance must not be null | High | Regulatory Reporting Owner | 1 |
| CTRL-007 | Account status must be valid | Medium | Account Data Owner | 292 |
| CTRL-004 | Customer country must be valid | Medium | Customer Data Owner | 51 |
| CTRL-002 | Customer name must not be null | Medium | Customer Data Owner | 1 |

## Remediation Workflow

Failed controls are converted into a remediation action log.

Each remediation item includes:

| Field | Description |
| --- | --- |
| control_id | Failed control identifier |
| check_name | Name of the failed control |
| table_name | Impacted table |
| dimension | Data quality dimension |
| severity | Severity of the issue |
| priority | Remediation priority |
| failed_count | Number of failed records |
| owner | Assigned data owner |
| regulatory_relevance | Reporting or governance impact |
| remediation_status | Current remediation status |
| target_resolution_days | Target number of days to resolve |
| recommended_action | Suggested remediation action |
| created_timestamp | Timestamp when the action was created |

Example priority logic:

| Priority | Criteria | Target Resolution |
| --- | --- | ---: |
| P1 | High severity failure | 2 days |
| P2 | Medium severity with 100+ failed records | 5 days |
| P3 | Medium severity with fewer than 100 failed records | 10 days |
| P4 | Low severity or informational issue | 15 days |

## Project Structure

```text
agentic-finance-data-governance/
├── config/
│   └── control_inventory.csv
├── data/
│   ├── raw/
│   └── warehouse/
├── outputs/
│   ├── data_quality/
│   ├── exceptions/
│   ├── remediation/
│   └── scorecards/
├── src/
│   ├── data_quality/
│   │   └── run_quality_checks.py
│   ├── exceptions/
│   │   └── export_dq_exceptions.py
│   ├── ingestion/
│   │   ├── generate_sample_data.py
│   │   ├── load_to_duckdb.py
│   │   └── validate_duckdb_load.py
│   ├── pipeline/
│   │   └── run_pipeline.py
│   ├── remediation/
│   │   └── build_remediation_log.py
│   └── reporting/
│       └── build_governance_scorecard.py
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Apate119/agentic-finance-data-governance.git
cd agentic-finance-data-governance
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or use the Makefile:

```bash
make install
```

### 4. Run the full pipeline

```bash
python src/pipeline/run_pipeline.py
```

Or use the Makefile:

```bash
make run
```


## Pipeline Steps

The full pipeline runner executes the following steps:

| Step | Script |
| --- | --- |
| Generate sample source data | `src/ingestion/generate_sample_data.py` |
| Load source data to DuckDB | `src/ingestion/load_to_duckdb.py` |
| Validate DuckDB staging tables | `src/ingestion/validate_duckdb_load.py` |
| Run data quality checks | `src/data_quality/run_quality_checks.py` |
| Build governance scorecard | `src/reporting/build_governance_scorecard.py` |
| Export DQ exceptions | `src/exceptions/export_dq_exceptions.py` |
| Build remediation action log | `src/remediation/build_remediation_log.py` |

## Main Outputs

| Output | Description |
| --- | --- |
| `data/raw/*.csv` | Synthetic source datasets |
| `data/warehouse/finance_governance.duckdb` | Local DuckDB warehouse |
| `outputs/data_quality/quality_check_results.csv` | Data quality results by control |
| `outputs/scorecards/governance_scorecard.csv` | Executive governance scorecard |
| `outputs/scorecards/dq_exception_summary.csv` | Failed controls grouped by control metadata |
| `outputs/scorecards/dq_results_enriched.csv` | DQ results joined to the control inventory |
| `outputs/exceptions/*.csv` | Exception-level failed records |
| `outputs/exceptions/exception_export_summary.csv` | Summary of exception files exported |
| `outputs/remediation/remediation_action_log.csv` | Owner-assigned remediation action log |

## Example Governance Outcome

The pipeline identified high-severity failures in account-to-customer integrity, transaction-to-account integrity, and regulatory balance completeness.

These failures were automatically:

1. Captured in the data quality results
2. Reflected in the governance scorecard
3. Enriched with owner and regulatory relevance metadata
4. Exported as exception-level CSV files
5. Routed into a remediation action log with priority and recommended actions

This mirrors a real-world finance data governance workflow where regulatory reporting datasets must be monitored, scored, and remediated before submission.

## Current Implementation

The current version runs locally using Python, pandas, DuckDB, and CSV-based inputs and outputs.

Enterprise platform integrations such as Snowflake, Databricks, dbt, orchestration, dashboards, and LLM-based remediation workflows are listed as future enhancements.

## Why This Project Matters

This project demonstrates practical experience with:

* Data governance operating models
* Data quality control design
* Regulatory reporting readiness
* Control inventory management
* Exception management
* Remediation workflow design
* Python-based data automation
* Local warehouse development using DuckDB
* Scalable project architecture for future cloud or enterprise data platforms

## Future Enhancements

Planned improvements include:

* Add schema validation before DQ execution
* Move DQ rules from hardcoded Python into a configurable rules file
* Add reference data tables for country, account status, and currency validation
* Add dbt-style transformations
* Add dashboard visualizations
* Add Snowflake or Databricks support
* Add automated lineage documentation
* Add historical trend tracking for control pass rates
* Add SLA monitoring for remediation aging
* Add agentic remediation recommendations using LLM workflows
