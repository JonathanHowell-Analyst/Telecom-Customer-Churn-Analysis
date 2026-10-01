"""
Telecom Customer Churn Analysis
Jonathan Howell

Portfolio reconstruction of the original customer churn analysis
completed as part of a Data Analytics Weiterbildung.

The original Jupyter Notebook is no longer available. This script
reconstructs the analytical approach using code preserved in the
original project PDF.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import statsmodels.formula.api as smf


# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

# Connect to the original SQLite database.
# Note: the original database is not included in this repository.
connection = sqlite3.connect("telco_churn.db")

# Load customer churn data.
df = pd.read_sql_query(
    "SELECT * FROM churn_data",
    connection
)

# Load city information.
cities_df = pd.read_sql_query(
    "SELECT * FROM cities",
    connection
)

# Combine the customer data with the corresponding city.
df = pd.merge(
    df,
    cities_df,
    left_on="local_area_code",
    right_on="area_code",
    how="left"
)

connection.close()

print("Dataset loaded successfully")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# --------------------------------------------------
# 2. DATA CLEANING
# --------------------------------------------------

# Check the dataset for missing values.
print("\nMissing values before cleaning:")
print(df.isna().sum())

# Negative customer service call counts are invalid.
# Convert these impossible values to missing values.
df.loc[
    df["customer_service_calls"] < 0,
    "customer_service_calls"
] = np.nan

# Replace missing customer service call values with the median.
service_calls_median = df["customer_service_calls"].median()

df["customer_service_calls"] = (
    df["customer_service_calls"]
    .fillna(service_calls_median)
)


# --------------------------------------------------
# 3. GEOGRAPHIC CHURN ANALYSIS
# --------------------------------------------------

# Calculate the churn rate for each city.
city_churn = (
    df.groupby("city")["churn"]
    .mean()
    .sort_values(ascending=False)
)

# Select the four cities with the highest churn rates.
top_four_cities = city_churn.head(4)

print("\nTop 4 Cities by Churn Rate:")
print(top_four_cities)

print("\nCustomer service calls cleaned.")


# --------------------------------------------------
# 4. CATEGORICAL CHURN ANALYSIS
# --------------------------------------------------

# Compare churn rates for the two categorical variables.
international_plan_churn = (
    df.groupby("international_plan")["churn"]
    .mean()
)

voice_mail_plan_churn = (
    df.groupby("voice_mail_plan")["churn"]
    .mean()
)

print("\nInternational Plan Churn Rates:")
print(international_plan_churn)

print("\nVoice Mail Plan Churn Rates:")
print(voice_mail_plan_churn)

# Identify active international-plan customers
# as a potential retention target group.
international_plan_targets = df[
    (df["international_plan"] == "yes") &
    (df["churn"] == 0)
]

print(
    f"\nActive international-plan customers: "
    f"{len(international_plan_targets)}"
)


# --------------------------------------------------
# 5. CUSTOMER SERVICE CALL ANALYSIS
# --------------------------------------------------

# Calculate churn rate by number of customer service calls.
service_call_churn = (
    df.groupby("customer_service_calls")["churn"]
    .mean()
)

print("\nChurn Rate by Customer Service Calls:")
print(service_call_churn)

# Customers making more than three service calls
# showed increased churn risk in the analysis.
service_call_threshold = 3

# Identify customers who have exceeded the threshold
# but are still active customers.
high_risk_service_customers = df[
    (df["customer_service_calls"] > service_call_threshold) &
    (df["churn"] == 0)
]

print(
    f"\nActive customers with more than "
    f"{service_call_threshold} service calls: "
    f"{len(high_risk_service_customers)}"
)
