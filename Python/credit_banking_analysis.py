import pandas as pd
from sqlalchemy import create_engine, text


# ============================================================
# CREDIT BANKING PROJECT - SQL + PYTHON ANALYSIS
# ============================================================

PROJECT_PATH = r"T:\Love\My coding\Credit_Banking_Project"

TRANSACTION_FILE = PROJECT_PATH + r"\cleaned_transactions.csv"
CUSTOMER_FILE = PROJECT_PATH + r"\cleaned_customers.csv"


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

transactions = pd.read_csv(TRANSACTION_FILE)
customers = pd.read_csv(CUSTOMER_FILE)

# Restore date columns after reading cleaned CSV files.
transactions["Date"] = pd.to_datetime(
    transactions["Date"],
    errors="coerce"
)

transactions["Return_date"] = pd.to_datetime(
    transactions["Return_date"],
    errors="coerce"
)

print("\nCleaned data loaded.")
print("Transactions:", transactions.shape)
print("Customers:", customers.shape)


# ============================================================
# 2. POSTGRESQL CONNECTION
# ============================================================
# Before running this section:
#   pip install sqlalchemy psycopg2-binary
#
# Change ONLY the values below to match your PostgreSQL setup.

DB_USER = "postgres"
DB_PASSWORD = "123456789"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credit_banking"

connection_string = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string)


# ============================================================
# 3. LOAD DATA INTO POSTGRESQL
# ============================================================
# This creates/replaces the two analysis tables.
#
# We keep the transaction rows as they are because the source
# contains repeated Transaction_ID values with return information.
# We do NOT drop duplicate transaction rows here.

transactions.to_sql(
    "transactions",
    engine,
    if_exists="replace",
    index=False
)

customers.to_sql(
    "customers",
    engine,
    if_exists="replace",
    index=False
)

print("\nData loaded into PostgreSQL successfully.")


# ============================================================
# 4. SQL ANALYSIS HELPER
# ============================================================

def run_sql(query, title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    result = pd.read_sql(text(query), engine)
    print(result.to_string(index=False))

    return result


# ============================================================
# 5. BASIC SQL DATA CHECKS
# ============================================================

run_sql(
    """
    SELECT
        COUNT(*) AS total_transaction_rows,
        COUNT(DISTINCT "Transaction_ID") AS unique_transaction_ids
    FROM transactions;
    """,
    "1. BASIC TRANSACTION SUMMARY"
)

run_sql(
    """
    SELECT COUNT(*) AS total_customers
    FROM customers;
    """,
    "2. TOTAL CUSTOMERS"
)


# ============================================================
# 6. CUSTOMER SEGMENTATION
# Required groups:
# Young Female, Mid-age Female, Old Female,
# Young Male, Mid-age Male, Old Male.
#
# Age boundaries are set here as:
# Young   = below 30
# Mid-age = 30 to 49
# Old     = 50 and above
# ============================================================

run_sql(
    """
    SELECT
        "Gender",
        CASE
            WHEN "Age" < 30 THEN 'Young'
            WHEN "Age" BETWEEN 30 AND 49 THEN 'Mid-age'
            ELSE 'Old'
        END AS age_group,
        COUNT(*) AS customer_count
    FROM customers
    WHERE "Age" IS NOT NULL
      AND "Gender" IS NOT NULL
    GROUP BY
        "Gender",
        CASE
            WHEN "Age" < 30 THEN 'Young'
            WHEN "Age" BETWEEN 30 AND 49 THEN 'Mid-age'
            ELSE 'Old'
        END
    ORDER BY "Gender", age_group;
    """,
    "3. CUSTOMER SEGMENTATION"
)


# ============================================================
# 7. SPENDING BY PRODUCT
# ============================================================

run_sql(
    """
    SELECT
        "Product_ID",
        ROUND(SUM("Selling_price")::numeric, 2) AS total_spending
    FROM transactions
    GROUP BY "Product_ID"
    ORDER BY total_spending DESC;
    """,
    "4. SPENDING BY PRODUCT"
)


# ============================================================
# 8. TOP 5 PRODUCTS BY SPENDING
# ============================================================

run_sql(
    """
    SELECT
        "Product_ID",
        ROUND(SUM("Selling_price")::numeric, 2) AS total_spending
    FROM transactions
    GROUP BY "Product_ID"
    ORDER BY total_spending DESC
    LIMIT 5;
    """,
    "5. TOP 5 PRODUCTS BY SPENDING"
)


# ============================================================
# 9. SPENDING BY STATE
# ============================================================

run_sql(
    """
    SELECT
        c."State",
        ROUND(SUM(t."Selling_price")::numeric, 2) AS total_spending
    FROM transactions t
    JOIN customers c
        ON t."Credit_card" = c."C_ID"
    WHERE c."State" IS NOT NULL
    GROUP BY c."State"
    ORDER BY total_spending DESC;
    """,
    "6. SPENDING BY STATE"
)


# ============================================================
# 10. TOP 5 STATES BY SPENDING
# ============================================================

run_sql(
    """
    SELECT
        c."State",
        ROUND(SUM(t."Selling_price")::numeric, 2) AS total_spending
    FROM transactions t
    JOIN customers c
        ON t."Credit_card" = c."C_ID"
    WHERE c."State" IS NOT NULL
    GROUP BY c."State"
    ORDER BY total_spending DESC
    LIMIT 5;
    """,
    "7. TOP 5 STATES BY SPENDING"
)


# ============================================================
# 11. SPENDING BY PAYMENT METHOD
# ============================================================

run_sql(
    """
    SELECT
        "Payment_Method",
        ROUND(SUM("Selling_price")::numeric, 2) AS total_spending
    FROM transactions
    GROUP BY "Payment_Method"
    ORDER BY total_spending DESC;
    """,
    "8. SPENDING BY PAYMENT METHOD"
)


# ============================================================
# 12. TOP 5 PAYMENT METHODS BY SPENDING
# ============================================================

run_sql(
    """
    SELECT
        "Payment_Method",
        ROUND(SUM("Selling_price")::numeric, 2) AS total_spending
    FROM transactions
    GROUP BY "Payment_Method"
    ORDER BY total_spending DESC
    LIMIT 5;
    """,
    "9. TOP 5 PAYMENT METHODS BY SPENDING"
)


# ============================================================
# 13. RETURN ANALYSIS BY STATE
# ============================================================

run_sql(
    """
    SELECT
        c."State",
        COUNT(*) FILTER (WHERE t."Return_ind" = 1) AS returned_rows,
        COUNT(*) AS total_rows,
        ROUND(
            (
                COUNT(*) FILTER (WHERE t."Return_ind" = 1) * 100.0
                / NULLIF(COUNT(*), 0)
            )::numeric,
            2
        ) AS return_rate_percent
    FROM transactions t
    JOIN customers c
        ON t."Credit_card" = c."C_ID"
    WHERE c."State" IS NOT NULL
    GROUP BY c."State"
    ORDER BY return_rate_percent DESC;
    """,
    "10. RETURN ANALYSIS BY STATE"
)


# ============================================================
# 14. RETURN ANALYSIS BY AGE GROUP
# ============================================================

run_sql(
    """
    SELECT
        CASE
            WHEN c."Age" < 30 THEN 'Young'
            WHEN c."Age" BETWEEN 30 AND 49 THEN 'Mid-age'
            ELSE 'Old'
        END AS age_group,
        COUNT(*) FILTER (WHERE t."Return_ind" = 1) AS returned_rows,
        COUNT(*) AS total_rows,
        ROUND(
            (
                COUNT(*) FILTER (WHERE t."Return_ind" = 1) * 100.0
                / NULLIF(COUNT(*), 0)
            )::numeric,
            2
        ) AS return_rate_percent
    FROM transactions t
    JOIN customers c
        ON t."Credit_card" = c."C_ID"
    WHERE c."Age" IS NOT NULL
    GROUP BY
        CASE
            WHEN c."Age" < 30 THEN 'Young'
            WHEN c."Age" BETWEEN 30 AND 49 THEN 'Mid-age'
            ELSE 'Old'
        END
    ORDER BY return_rate_percent DESC;
    """,
    "11. RETURN ANALYSIS BY AGE GROUP"
)


# ============================================================
# 15. RETURN ANALYSIS BY CONDITION
# ============================================================

run_sql(
    """
    SELECT
        "Condition",
        COUNT(*) FILTER (WHERE "Return_ind" = 1) AS returned_rows,
        COUNT(*) AS total_rows,
        ROUND(
            (
                COUNT(*) FILTER (WHERE "Return_ind" = 1) * 100.0
                / NULLIF(COUNT(*), 0)
            )::numeric,
            2
        ) AS return_rate_percent
    FROM transactions
    GROUP BY "Condition"
    ORDER BY return_rate_percent DESC;
    """,
    "12. RETURN ANALYSIS BY CONDITION"
)


# ============================================================
# 16. RETURN ANALYSIS BY PRODUCT CATEGORY
# ============================================================

run_sql(
    """
    SELECT
        "P_CATEGORY",
        COUNT(*) FILTER (WHERE "Return_ind" = 1) AS returned_rows,
        COUNT(*) AS total_rows,
        ROUND(
            (
                COUNT(*) FILTER (WHERE "Return_ind" = 1) * 100.0
                / NULLIF(COUNT(*), 0)
            )::numeric,
            2
        ) AS return_rate_percent
    FROM transactions
    GROUP BY "P_CATEGORY"
    ORDER BY return_rate_percent DESC;
    """,
    "13. RETURN ANALYSIS BY PRODUCT CATEGORY"
)


# ============================================================
# 17. RETURN ANALYSIS BY DISCOUNT STATUS
# ============================================================

run_sql(
    """
    SELECT
        CASE
            WHEN "Coupon_ID" IS NOT NULL THEN 'Coupon'
            ELSE 'No Coupon'
        END AS discount_status,
        COUNT(*) FILTER (WHERE "Return_ind" = 1) AS returned_rows,
        COUNT(*) AS total_rows,
        ROUND(
            (
                COUNT(*) FILTER (WHERE "Return_ind" = 1) * 100.0
                / NULLIF(COUNT(*), 0)
            )::numeric,
            2
        ) AS return_rate_percent
    FROM transactions
    GROUP BY
        CASE
            WHEN "Coupon_ID" IS NOT NULL THEN 'Coupon'
            ELSE 'No Coupon'
        END
    ORDER BY return_rate_percent DESC;
    """,
    "14. RETURN ANALYSIS BY DISCOUNT STATUS"
)


# ============================================================
# 18. ORDER TIMING PROFILE
# ============================================================

run_sql(
    """
    SELECT
        EXTRACT(HOUR FROM "Time"::time) AS order_hour,
        COUNT(*) AS order_rows
    FROM transactions
    WHERE "Time" IS NOT NULL
    GROUP BY EXTRACT(HOUR FROM "Time"::time)
    ORDER BY order_hour;
    """,
    "15. ORDER TIMING PROFILE BY HOUR"
)


# ============================================================
# 19. PAYMENT METHOD PROVIDING MORE DISCOUNT
#
# Discount amount = Price - Selling_price
# ============================================================

run_sql(
    """
    SELECT
        "Payment_Method",
        ROUND(SUM("Price" - "Selling_price")::numeric, 2)
            AS total_discount,
        ROUND(AVG("Price" - "Selling_price")::numeric, 2)
            AS average_discount
    FROM transactions
    WHERE "Price" IS NOT NULL
      AND "Selling_price" IS NOT NULL
    GROUP BY "Payment_Method"
    ORDER BY total_discount DESC;
    """,
    "16. PAYMENT METHOD PROVIDING MORE DISCOUNT"
)


# ============================================================
# 20. HIGH-VALUE VS LOW-VALUE ITEMS
#
# This uses the median selling price as the split point.
# This avoids inventing an arbitrary monetary threshold.
# ============================================================

run_sql(
    """
    WITH price_median AS (
        SELECT
            PERCENTILE_CONT(0.5)
            WITHIN GROUP (ORDER BY "Selling_price") AS median_price
        FROM transactions
        WHERE "Selling_price" IS NOT NULL
    )
    SELECT
        CASE
            WHEN t."Selling_price" >= p.median_price
                THEN 'High Value'
            ELSE 'Low Value'
        END AS value_group,
        COUNT(*) AS order_rows,
        COUNT(DISTINCT t."Transaction_ID") AS transaction_count,
        ROUND(SUM(t."Selling_price")::numeric, 2)
            AS total_spending
    FROM transactions t
    CROSS JOIN price_median p
    GROUP BY
        CASE
            WHEN t."Selling_price" >= p.median_price
                THEN 'High Value'
            ELSE 'Low Value'
        END
    ORDER BY value_group;
    """,
    "17. HIGH-VALUE VS LOW-VALUE ITEMS"
)


# ============================================================
# 21. DISCOUNT VS NUMBER OF ORDERS
# ============================================================

run_sql(
    """
    SELECT
        ROUND(("Price" - "Selling_price")::numeric, 2)
            AS discount_amount,
        COUNT(*) AS order_rows,
        COUNT(DISTINCT "Transaction_ID") AS transaction_count
    FROM transactions
    WHERE "Price" IS NOT NULL
      AND "Selling_price" IS NOT NULL
    GROUP BY ROUND(("Price" - "Selling_price")::numeric, 2)
    ORDER BY discount_amount;
    """,
    "18. DISCOUNT VS NUMBER OF ORDERS"
)


# ============================================================
# 22. DISCOUNT BUCKETS VS NUMBER OF ORDERS
# ============================================================

run_sql(
    """
    SELECT
        CASE
            WHEN ("Price" - "Selling_price") <= 0 THEN 'No Discount'
            WHEN ("Price" - "Selling_price") < 50 THEN 'Below 50'
            WHEN ("Price" - "Selling_price") < 100 THEN '50 to 99.99'
            WHEN ("Price" - "Selling_price") < 250 THEN '100 to 249.99'
            ELSE '250 or More'
        END AS discount_bucket,
        COUNT(*) AS order_rows,
        COUNT(DISTINCT "Transaction_ID") AS transaction_count
    FROM transactions
    WHERE "Price" IS NOT NULL
      AND "Selling_price" IS NOT NULL
    GROUP BY
        CASE
            WHEN ("Price" - "Selling_price") <= 0 THEN 'No Discount'
            WHEN ("Price" - "Selling_price") < 50 THEN 'Below 50'
            WHEN ("Price" - "Selling_price") < 100 THEN '50 to 99.99'
            WHEN ("Price" - "Selling_price") < 250 THEN '100 to 249.99'
            ELSE '250 or More'
        END
    ORDER BY
        MIN("Price" - "Selling_price");
    """,
    "19. DISCOUNT BUCKETS VS NUMBER OF ORDERS"
)


print("\n" + "=" * 70)
print("ALL SQL ANALYSIS COMPLETED")
print("=" * 70)
