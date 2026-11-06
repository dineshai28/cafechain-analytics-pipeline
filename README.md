# CafeChain Analytics Engineering Pipeline

An end-to-end ETL (Extract, Transform, Load) pipeline built to ingest messy raw data, validate it against strict data contracts, and separate it into clean and quarantine tables to prevent data loss.

## Tech Stack
- **Python (pandas)**: For extracting raw Excel data.
- **DuckDB**: An in-process analytical database used as the local data warehouse.
- **SQL**: For data validation, quarantine logic, and audit summaries.

## The Problem
Raw transactional data often contains nulls, negative values, future dates, and orphan keys. If this data reaches a dashboard, the business makes bad decisions.

## The Solution (Data Contracts & Quarantine)
This pipeline enforces the following rules on `raw_orders`:
1. `quantity` cannot be null.
2. `unit_price` cannot be negative.
3. `order_date` cannot be in the future.
4. `store_id` must exist in the `raw_stores` table (no orphan keys).

Rows that fail these rules are routed to a `quarantine_orders` table with a written `bad_reason`. Clean rows are routed to `clean_orders`.

## The Audit Trail (No Silent Data Loss)
The pipeline generates a `pipeline_summary` table that proves the math:
- **Rows In:** 35
- **Rows Passed:** 26
- **Rows Quarantined:** 9
*(35 = 26 + 9. No rows disappeared.)*

## How to Run
1. Clone this repo.
2. Install requirements: `pip install pandas duckdb openpyxl`
3. Run the pipeline: `python etl.py`