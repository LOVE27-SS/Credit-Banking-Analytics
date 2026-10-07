import pandas as pd

# ============================================================
# CREDIT BANKING PROJECT - DATA CLEANING
# ============================================================

PROJECT_PATH = r"T:\Love\My coding\Credit_Banking_Project"

TRANSACTION_FILE = PROJECT_PATH + r"\Project_2.csv"
CUSTOMER_FILE = PROJECT_PATH + r"\Customer_Info.csv"

CLEANED_TRANSACTION_FILE = PROJECT_PATH + r"\cleaned_transactions.csv"
CLEANED_CUSTOMER_FILE = PROJECT_PATH + r"\cleaned_customers.csv"


# ============================================================
# 1. READ CSV FILES
# ============================================================

transactions = pd.read_csv(TRANSACTION_FILE)
customers = pd.read_csv(CUSTOMER_FILE)


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

transactions.columns = (
    transactions.columns
    .str.strip()
    .str.replace(" ", "_", regex=False)
)

customers.columns = (
    customers.columns
    .str.strip()
    .str.replace(" ", "_", regex=False)
)

# Keep the original spelling from the source data.
# The source contains CONDTION rather than CONDITION.
if "CONDTION" in transactions.columns:
    transactions = transactions.rename(columns={"CONDTION": "Condition"})


# ============================================================
# 3. REMOVE COMPLETELY BLANK CUSTOMER ROWS
# ============================================================

customers = customers.dropna(how="all").copy()


# ============================================================
# 4. CLEAN PRICE AND SELLING PRICE
# ============================================================

for column in ["Price", "Selling_price"]:
    transactions[column] = (
        transactions[column]
        .astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("(", "-", regex=False)
        .str.replace(")", "", regex=False)
        .str.strip()
    )
    transactions[column] = pd.to_numeric(
        transactions[column],
        errors="coerce"
    )


# ============================================================
# 5. CONVERT DATE COLUMNS
# ============================================================

transactions["Date"] = pd.to_datetime(
    transactions["Date"],
    format="%d/%m/%Y",
    errors="coerce"
)

transactions["Return_date"] = pd.to_datetime(
    transactions["Return_date"],
    format="%d-%m-%Y",
    errors="coerce"
)


# ============================================================
# 6. APPLY 5% DISCOUNT RULE
# If Coupon_ID exists but Price = Selling_price,
# Selling_price should be 95% of Price.
# ============================================================

coupon_price_same = (
    transactions["Coupon_ID"].notna()
    & (transactions["Price"] == transactions["Selling_price"])
)

transactions.loc[coupon_price_same, "Selling_price"] = (
    transactions.loc[coupon_price_same, "Price"] * 0.95
)


# ============================================================
# 7. DATA-QUALITY FLAGS
# ============================================================

transactions["Invalid_Return_Date"] = (
    transactions["Return_date"].notna()
    & (transactions["Return_date"] < transactions["Date"])
)

transactions["NoCoupon_PriceMismatch"] = (
    transactions["Coupon_ID"].isna()
    & (transactions["Price"] != transactions["Selling_price"])
)

transactions["Duplicate_Transaction_ID"] = (
    transactions["Transaction_ID"].duplicated(keep=False)
)


# ============================================================
# 8. UNDER-18 CREDIT CARDHOLDER FLAG
# ============================================================

under_18_customer_ids = customers.loc[
    customers["Age"] < 18, "C_ID"
]

transactions["Under18_Cardholder"] = (
    transactions["Credit_card"].notna()
    & transactions["Credit_card"].isin(under_18_customer_ids)
)


# ============================================================
# 9. REPORT DATA-QUALITY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("CREDIT BANKING PROJECT - CLEANING SUMMARY")
print("=" * 60)

print("\nTransaction rows:", len(transactions))
print("Customer rows:", len(customers))

print("\nBlank Credit Card:", transactions["Credit_card"].isna().sum())
print("Missing Coupon ID:", transactions["Coupon_ID"].isna().sum())

print("\n5% coupon corrections:", int(coupon_price_same.sum()))
print(
    "Coupon + same price remaining:",
    int(
        (
            transactions["Coupon_ID"].notna()
            & (transactions["Price"] == transactions["Selling_price"])
        ).sum()
    )
)

print(
    "\nNo-coupon price mismatches:",
    int(transactions["NoCoupon_PriceMismatch"].sum())
)

print(
    "Invalid return dates:",
    int(transactions["Invalid_Return_Date"].sum())
)

print(
    "Under-18 customers:",
    int((customers["Age"] < 18).sum())
)

print(
    "Transactions linked to under-18 cardholders:",
    int(transactions["Under18_Cardholder"].sum())
)

print(
    "\nUnique Transaction IDs:",
    transactions["Transaction_ID"].nunique()
)

print(
    "Transaction IDs appearing more than once:",
    int(
        transactions["Transaction_ID"]
        .value_counts()
        .gt(1)
        .sum()
    )
)

print(
    "Completely blank customer rows removed:",
    202 - len(customers)
)


# ============================================================
# 10. SAVE CLEANED DATA
# ============================================================

transactions.to_csv(
    CLEANED_TRANSACTION_FILE,
    index=False
)

customers.to_csv(
    CLEANED_CUSTOMER_FILE,
    index=False
)

print("\nCleaned files saved successfully:")
print(CLEANED_TRANSACTION_FILE)
print(CLEANED_CUSTOMER_FILE)
