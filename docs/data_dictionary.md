cat > docs/data_dictionary.md <<'EOF'
# Data Dictionary

## Overview

This document describes the synthetic datasets used in the Agentic Finance Data Governance Pipeline.

The project currently includes four source datasets:

* `customers.csv`
* `accounts.csv`
* `transactions.csv`
* `regulatory_balances.csv`

All source data is synthetically generated and does not contain confidential, customer, or production financial information.

## customers.csv

Customer reference data used to support account ownership, customer segmentation, and regulatory reporting traceability.

| Field | Description | Example |
| --- | --- | --- |
| customer_id | Unique identifier for each customer | CUST0001 |
| customer_name | Customer name | John Smith |
| customer_segment | Customer segment or classification | Retail |
| country | Customer country | US |
| created_date | Date the customer record was created | 2024-01-15 |

## accounts.csv

Account master data used to connect customers to financial accounts.

| Field | Description | Example |
| --- | --- | --- |
| account_id | Unique identifier for each account | ACC0001 |
| customer_id | Customer identifier linked to the account | CUST0001 |
| account_type | Type of financial account | Checking |
| account_status | Current lifecycle status of the account | Active |
| open_date | Date the account was opened | 2024-02-01 |

## transactions.csv

Transaction-level activity used to validate financial activity and account-level traceability.

| Field | Description | Example |
| --- | --- | --- |
| transaction_id | Unique identifier for each transaction | TXN000001 |
| account_id | Account identifier linked to the transaction | ACC0001 |
| transaction_date | Date the transaction occurred | 2024-03-10 |
| transaction_type | Type of transaction activity | Deposit |
| amount | Transaction amount | 250.75 |
| currency | Currency of the transaction | USD |

## regulatory_balances.csv

Regulatory reporting balance data used to simulate reporting readiness checks.

| Field | Description | Example |
| --- | --- | --- |
| report_date | Date associated with the regulatory report balance | 2024-03-31 |
| account_type | Account type included in the regulatory balance | Checking |
| reported_balance | Reported financial balance | 125000.50 |
| report_name | Name of the regulatory report | FFIEC 031 |

## Relationship Overview

The datasets are connected through customer and account relationships:

    customers.customer_id
            ↓
    accounts.customer_id

    accounts.account_id
            ↓
    transactions.account_id

These relationships support integrity checks such as:

* Every account must map to a valid customer
* Every transaction must map to a valid account

## Data Quality Relevance

The fields in these datasets support controls across three data quality dimensions:

| Dimension | Example Fields | Example Controls |
| --- | --- | --- |
| Completeness | `customer_id`, `account_id`, `transaction_id`, `reported_balance` | Required fields must not be null |
| Validity | `country`, `account_status`, `currency`, `reported_balance` | Values must match approved domains or expected ranges |
| Integrity | `customer_id`, `account_id` | Child records must map to valid parent records |

## Summary

This data dictionary provides a business-readable view of the synthetic datasets used by the pipeline.

It helps reviewers understand the data model, key fields, relationships, and data quality relevance before reviewing the control logic or output files.
EOF