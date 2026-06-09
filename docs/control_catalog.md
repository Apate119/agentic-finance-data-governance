# Control Catalog

## Overview

This document describes the data quality controls used in the Agentic Finance Data Governance Pipeline.

Each control is mapped to a control ID, data quality dimension, severity, data owner, and regulatory relevance. The control catalog is maintained in `config/control_inventory.csv`.

## Control Dimensions

| Dimension | Description |
| --- | --- |
| Completeness | Validates that required fields are populated |
| Validity | Validates that values conform to approved formats, domains, or reference values |
| Integrity | Validates that relationships between datasets are complete and traceable |

## Control Severity

| Severity | Meaning |
| --- | --- |
| High | Issue could materially impact reporting completeness, traceability, or regulatory readiness |
| Medium | Issue creates data quality risk but may be remediated through review or reference data correction |
| Low | Issue is informational or lower impact |

## Control Catalog

| Control ID | Control Name | Dimension | Severity | Business Purpose |
| --- | --- | --- | --- | --- |
| CTRL-001 | Customer ID must not be null | Completeness | High | Ensures every customer record has a unique customer identifier |
| CTRL-002 | Customer name must not be null | Completeness | Medium | Ensures customer reference data is complete for business review |
| CTRL-003 | Customer created date must not be null | Completeness | Medium | Ensures customer onboarding records have traceable creation dates |
| CTRL-004 | Customer country must be valid | Validity | Medium | Ensures customer country values align to approved reporting domains |
| CTRL-005 | Account ID must not be null | Completeness | High | Ensures every account record has a unique account identifier |
| CTRL-006 | Every account must map to a valid customer | Integrity | High | Confirms account records can be traced back to valid customer records |
| CTRL-007 | Account status must be valid | Validity | Medium | Ensures account lifecycle statuses align to approved values |
| CTRL-008 | Account open date must not be null | Completeness | Medium | Ensures account records include traceable opening dates |
| CTRL-009 | Transaction ID must not be null | Completeness | High | Ensures every transaction has a unique transaction identifier |
| CTRL-010 | Every transaction must map to a valid account | Integrity | High | Confirms transaction activity can be traced back to valid accounts |
| CTRL-011 | Transaction amount must be positive | Validity | Medium | Ensures transaction amounts are reasonable for reporting and analytics |
| CTRL-012 | Transaction currency must be valid | Validity | Medium | Ensures transaction currencies align to approved reporting values |
| CTRL-013 | Regulatory report date must not be null | Completeness | High | Ensures regulatory balance records are tied to a reporting date |
| CTRL-014 | Regulatory reported balance must not be null | Completeness | High | Ensures reported balances are populated for regulatory reporting |
| CTRL-015 | Regulatory reported balance must be non-negative | Validity | High | Ensures reported balances meet expected regulatory reporting constraints |
| CTRL-016 | Regulatory account type must be valid | Validity | Medium | Ensures regulatory account types align to approved reporting categories |
| CTRL-017 | Regulatory report name must be valid | Validity | Medium | Ensures records are mapped to approved regulatory report names |

## Governance Usage

The control catalog supports:

* Consistent control execution
* Clear ownership assignment
* Severity-based prioritization
* Regulatory relevance documentation
* Exception routing and remediation tracking
* Executive reporting through governance scorecards

## Future Enhancements

Future versions of the project can move control logic into a fully configurable rules framework, allowing new controls to be added without changing Python code.