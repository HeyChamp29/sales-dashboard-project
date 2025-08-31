# 📌 Task 3: Identifying Customers Who Completed Checkout but Didn't Pay (2022)

import pandas as pd
import os

# Step 1: Load Dataset
import pandas as pd

# ✅ Correct path
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"

# Load CSV
df = pd.read_csv(file_path)

print(df.head())  # just to confirm it's loading fine
  # <-- Update if needed
df = pd.read_csv(file_path)

# Step 2: Ensure order_date is datetime & extract year
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['year'] = df['order_date'].dt.year

# Step 3: Filter for customers who completed checkout but didn’t pay
# Conditions: is_gross = 1 (checkout done), is_valid = 0 (not valid), is_net = 0 (no payment), year = 2022
filtered_df = df[
    (df['is_gross'] == 1) &
    (df['is_valid'] == 0) &
    (df['is_net'] == 0) &
    (df['year'] == 2022)
]

# Step 4: Select required columns & remove duplicates
customers = filtered_df[['customer_id', 'registered_date']].drop_duplicates()

# Step 5: Display Results
print("👥 Customers who completed checkout but didn’t pay in 2022:")
print(customers.head(20))   # show first 20 as preview

# Step 6: Save Results for Marketing Team
customers.to_csv("customers_no_payment_2022.csv", index=False)
print("✅ File saved: customers_no_payment_2022.csv")
