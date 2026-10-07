-- ==========================================
-- CREDIT BANKING PROJECT
-- SQL ANALYSIS
-- ==========================================


-- 1. BASIC DATA SUMMARY
-- ==========================================

SELECT COUNT(*) AS total_transactions
FROM transactions;

SELECT COUNT(*) AS total_customers
FROM customers;


-- 2. CUSTOMER SEGMENTATION
-- ==========================================

SELECT
    "Gender",
    CASE
        WHEN "Age" < 30 THEN 'Young'
        WHEN "Age" BETWEEN 30 AND 49 THEN 'Mid-age'
        ELSE 'Old'
    END AS age_group,
    COUNT(*) AS customer_count
FROM customers
GROUP BY
    "Gender",
    CASE
        WHEN "Age" < 30 THEN 'Young'
        WHEN "Age" BETWEEN 30 AND 49 THEN 'Mid-age'
        ELSE 'Old'
    END
ORDER BY
    "Gender",
    age_group;


-- 3. SPENDING BY PRODUCT CATEGORY
-- ==========================================

SELECT
    "P_CATEGORY" AS product_category,
    SUM("Selling_price") AS total_spending
FROM transactions
GROUP BY "P_CATEGORY"
ORDER BY total_spending DESC;


-- 4. TOP 5 PRODUCT CATEGORIES
-- ==========================================

SELECT
    "P_CATEGORY" AS product_category,
    SUM("Selling_price") AS total_spending
FROM transactions
GROUP BY "P_CATEGORY"
ORDER BY total_spending DESC
LIMIT 5;


-- 5. SPENDING BY STATE
-- ==========================================

SELECT
    c."State",
    SUM(t."Selling_price") AS total_spending
FROM transactions t
JOIN customers c
    ON t."Credit_card" = c."C_ID"
GROUP BY c."State"
ORDER BY total_spending DESC;


-- 6. TOP 5 STATES
-- ==========================================

SELECT
    c."State",
    SUM(t."Selling_price") AS total_spending
FROM transactions t
JOIN customers c
    ON t."Credit_card" = c."C_ID"
GROUP BY c."State"
ORDER BY total_spending DESC
LIMIT 5;


-- 7. SPENDING BY PAYMENT METHOD
-- ==========================================

SELECT
    "Payment_Method",
    SUM("Selling_price") AS total_spending
FROM transactions
GROUP BY "Payment_Method"
ORDER BY total_spending DESC;


-- 8. TOP 5 PAYMENT METHODS
-- ==========================================

SELECT
    "Payment_Method",
    SUM("Selling_price") AS total_spending
FROM transactions
GROUP BY "Payment_Method"
ORDER BY total_spending DESC
LIMIT 5;


-- 9. RETURN ANALYSIS BY STATE
-- ==========================================

SELECT
    c."State",
    COUNT(*) AS returned_orders
FROM transactions t
JOIN customers c
    ON t."Credit_card" = c."C_ID"
WHERE t."Return_ind" = 1
GROUP BY c."State"
ORDER BY returned_orders DESC;


-- 10. RETURN ANALYSIS BY AGE GROUP
-- ==========================================

SELECT
    CASE
        WHEN c."Age" < 30 THEN 'Young'
        WHEN c."Age" BETWEEN 30 AND 49 THEN 'Mid-age'
        ELSE 'Old'
    END AS age_group,
    COUNT(*) AS returned_orders
FROM transactions t
JOIN customers c
    ON t."Credit_card" = c."C_ID"
WHERE t."Return_ind" = 1
GROUP BY
    CASE
        WHEN c."Age" < 30 THEN 'Young'
        WHEN c."Age" BETWEEN 30 AND 49 THEN 'Mid-age'
        ELSE 'Old'
    END
ORDER BY returned_orders DESC;


-- 11. RETURN ANALYSIS BY CONDITION
-- ==========================================

SELECT
    "Condition",
    COUNT(*) AS returned_orders
FROM transactions
WHERE "Return_ind" = 1
GROUP BY "Condition"
ORDER BY returned_orders DESC;


-- 12. RETURN ANALYSIS BY PRODUCT CATEGORY
-- ==========================================

SELECT
    "P_CATEGORY" AS product_category,
    COUNT(*) AS returned_orders
FROM transactions
WHERE "Return_ind" = 1
GROUP BY "P_CATEGORY"
ORDER BY returned_orders DESC;


-- 13. RETURN ANALYSIS BY DISCOUNT
-- ==========================================

SELECT
    CASE
        WHEN "Price" > "Selling_price" THEN 'Discounted'
        ELSE 'No Discount'
    END AS discount_status,
    COUNT(*) AS returned_orders
FROM transactions
WHERE "Return_ind" = 1
GROUP BY
    CASE
        WHEN "Price" > "Selling_price" THEN 'Discounted'
        ELSE 'No Discount'
    END
ORDER BY returned_orders DESC;


-- 14. ORDER TIMING PROFILE
-- ==========================================

SELECT
    EXTRACT(HOUR FROM "Time"::time) AS order_hour,
    COUNT(*) AS order_count
FROM transactions
GROUP BY order_hour
ORDER BY order_hour;


-- 15. DISCOUNT BY PAYMENT METHOD
-- ==========================================

SELECT
    "Payment_Method",
    SUM("Price" - "Selling_price") AS total_discount
FROM transactions
WHERE "Price" > "Selling_price"
GROUP BY "Payment_Method"
ORDER BY total_discount DESC;


-- 16. HIGH-VALUE VS LOW-VALUE ITEMS
-- ==========================================

WITH median_price AS (
    SELECT
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY "Selling_price") AS median_value
    FROM transactions
)
SELECT
    CASE
        WHEN "Selling_price" >= median_value THEN 'High-value'
        ELSE 'Low-value'
    END AS value_category,
    COUNT(*) AS order_count,
    SUM("Selling_price") AS total_spending
FROM transactions, median_price
GROUP BY
    CASE
        WHEN "Selling_price" >= median_value THEN 'High-value'
        ELSE 'Low-value'
    END
ORDER BY total_spending DESC;


-- 17. DISCOUNT VS NUMBER OF ORDERS
-- ==========================================

SELECT
    CASE
        WHEN ("Price" - "Selling_price") <= 0 THEN 'No Discount'
        WHEN ("Price" - "Selling_price") < 50 THEN 'Below 50'
        WHEN ("Price" - "Selling_price") < 100 THEN '50 to 99.99'
        ELSE '100 or More'
    END AS discount_bucket,
    COUNT(*) AS order_count
FROM transactions
GROUP BY
    CASE
        WHEN ("Price" - "Selling_price") <= 0 THEN 'No Discount'
        WHEN ("Price" - "Selling_price") < 50 THEN 'Below 50'
        WHEN ("Price" - "Selling_price") < 100 THEN '50 to 99.99'
        ELSE '100 or More'
    END
ORDER BY order_count DESC;


-- ==========================================
-- END OF SQL ANALYSIS
-- ==========================================