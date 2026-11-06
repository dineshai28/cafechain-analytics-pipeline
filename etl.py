import duckdb
import pandas as pd

# 1. Connect to database and read data
con = duckdb.connect("cafe_chain.duckdb")
sheets = pd.read_excel(r"C:\Users\dines\OneDrive\Desktop\CafeChain_dataset.xlsx", sheet_name=None)

# 2. Load raw_orders and clean up junk columns
orders_df = sheets['raw_orders']
orders_df = orders_df.loc[:, ~orders_df.columns.astype(str).str.contains("^Unnamed|Note", case=False, na=False)]
con.execute("CREATE OR REPLACE TABLE raw_orders AS SELECT * FROM orders_df")

# 3. Load raw_stores (needed for the orphan rule)
stores_df = sheets['raw_stores']
con.execute("CREATE OR REPLACE TABLE raw_stores AS SELECT * FROM stores_df")

# 4. Create the Quarantine Table
con.execute("""
    CREATE OR REPLACE TABLE quarantine_orders AS
    SELECT 
        *,
        CASE 
            WHEN quantity IS NULL THEN 'Quantity is missing'
            WHEN unit_price < 0 THEN 'Unit price is negative'
            WHEN order_date > CURRENT_DATE THEN 'Order date is in the future'
            WHEN store_id NOT IN (SELECT store_id FROM raw_stores) THEN 'Orphan store_id'
        END AS bad_reason
    FROM raw_orders
    WHERE 
        quantity IS NULL 
        OR unit_price < 0 
        OR order_date > CURRENT_DATE
        OR store_id NOT IN (SELECT store_id FROM raw_stores)
""")

# 5. Create the Clean Table
con.execute("""
    CREATE OR REPLACE TABLE clean_orders AS
    SELECT * FROM raw_orders
    WHERE 
        quantity IS NOT NULL 
        AND unit_price >= 0 
        AND order_date <= CURRENT_DATE
        AND store_id IN (SELECT store_id FROM raw_stores)
""")

# 6. Create the Summary Table
con.execute("""
    CREATE OR REPLACE TABLE pipeline_summary AS
    SELECT 
        'raw_orders' AS table_name,
        (SELECT COUNT(*) FROM raw_orders) AS rows_in,
        (SELECT COUNT(*) FROM clean_orders) AS rows_passed,
        (SELECT COUNT(*) FROM quarantine_orders) AS rows_quarantined;
""")

# 7. Print the summary
print("\nPipeline Complete! Here is the summary:")
summary = con.sql("SELECT * FROM pipeline_summary").df()
print(summary.to_string(index=False))

con.close()