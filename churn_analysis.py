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
