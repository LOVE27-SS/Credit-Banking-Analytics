# 💳 Credit Banking Analytics

An end-to-end **Credit Banking Analytics** project built using **Python, PostgreSQL, SQL, Pandas, Plotly and Streamlit**.

The project performs data cleaning, customer segmentation, spending analysis, return analysis, discount analysis and interactive visualization through a Streamlit dashboard.

## 📌 Project Overview

The goal of this project is to analyze credit banking transaction and customer data and identify useful business insights related to:

- Customer demographics and age groups
- Product category spending
- State-wise spending
- Payment method usage and spending
- Returned orders
- Order timing
- Discounts and payment methods
- High-value and low-value orders

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **PostgreSQL**
- **SQL**
- **SQLAlchemy**
- **Psycopg2**
- **Plotly**
- **Streamlit**
- **VS Code**
- **Git & GitHub**

## 📂 Project Structure

```text
Credit_Banking_Project/
│
├── Python/
│   ├── data_cleaning.py
│   └── credit_banking_analysis.py
│
├── SQL/
│   └── credit_banking.sql
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── Project_2.csv              # Local source data - not uploaded
├── Customer_Info.csv          # Local source data - not uploaded
├── cleaned_transactions.csv   # Generated locally - not uploaded
└── cleaned_customers.csv      # Generated locally - not uploaded
```

## 🔄 Project Workflow

```text
Raw CSV Data
     ↓
Data Cleaning & Validation
     ↓
Cleaned Transaction + Customer Data
     ↓
PostgreSQL Database
     ↓
SQL Analysis
     ↓
Python Analysis
     ↓
Streamlit Dashboard
```

## 🧹 Data Cleaning

The cleaning process includes:

- Checking missing values
- Checking blank credit card values
- Removing completely blank customer records
- Cleaning currency values
- Converting dates and numeric columns
- Applying the required 5% discount rule when a coupon exists but Price equals Selling Price
- Checking invalid return dates
- Checking customers below 18 years
- Checking duplicate Transaction IDs
- Checking transactions where no coupon exists but Price differs from Selling Price

## 👥 Customer Segmentation

Customers are divided into:

| Age Group | Age |
|---|---|
| Young | Below 30 |
| Mid-age | 30–49 |
| Old | 50+ |

The segmentation is further divided by gender:

- Young Female
- Mid-age Female
- Old Female
- Young Male
- Mid-age Male
- Old Male

## 📊 SQL Analysis

The PostgreSQL analysis covers:

1. Total transactions
2. Total customers
3. Customer segmentation
4. Spending by product category
5. Top 5 product categories
6. Spending by state
7. Top 5 states
8. Spending by payment method
9. Top 5 payment methods
10. Returns by state
11. Returns by age group
12. Returns by product condition
13. Returns by product category
14. Returns by discount status
15. Order timing by hour
16. Discount by payment method
17. High-value vs low-value orders
18. Discount amount vs order count

## 📈 Streamlit Dashboard

The Streamlit dashboard provides interactive visualization for:

### Overview
- Total transactions
- Total spending
- Total discount
- Returned orders
- Spending by product category
- Spending by payment method
- Spending by state

### Customer Analysis
- Gender distribution
- Age-group distribution
- Gender + age-group segmentation

### Sales Analysis
- Top 5 product categories
- High-value vs low-value orders
- Orders by hour

### Return Analysis
- Returns by state
- Returns by age group
- Returns by product condition
- Returns by product category

### Discount Analysis
- Discount by payment method
- Discount amount vs number of orders

## ▶️ How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Credit_Banking_Project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the data

Place the original CSV files in the project root:

```text
Project_2.csv
Customer_Info.csv
```

Run:

```bash
python Python/data_cleaning.py
```

This generates:

```text
cleaned_transactions.csv
cleaned_customers.csv
```

### 4. PostgreSQL

Create a PostgreSQL database named:

```text
credit_banking
```

Update the PostgreSQL username/password in the Python analysis script before running it.

Then run:

```bash
python Python/credit_banking_analysis.py
```

### 5. Run the Streamlit dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## 🔐 Data Privacy

The original datasets contain customer-related information. For this reason, the raw CSV files and generated customer datasets are excluded from the GitHub repository using `.gitignore`.

Do not upload:

- Customer names
- Email addresses
- Mobile numbers
- Addresses
- Credit card/customer identifiers
- Database passwords

For a public portfolio repository, use anonymized or sample data instead.

## 📌 Key Findings

The analysis identifies differences in:

- Spending across product categories
- State-wise customer spending
- Payment method spending
- Return patterns
- Customer age groups
- Discount behavior
- Order timing
- High-value and low-value purchases

The exact values can be explored interactively through the Streamlit dashboard.

## 🚀 Future Improvements

- Add monthly/yearly sales trends
- Add advanced KPIs
- Add downloadable reports
- Add machine learning for customer segmentation
- Add return prediction
- Deploy the Streamlit dashboard online
- Add anonymized sample data for public demonstration

## 👨‍💻 Author

**Lovenesh Sharma**

Credit Banking Analytics Project

---

⭐ If you find this project useful, consider giving the repository a star.
