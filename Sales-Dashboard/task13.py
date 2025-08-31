import pandas as pd

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Convert order_date to datetime and filter for 2022
df['order_date'] = pd.to_datetime(df['order_date'])
df_2022 = df[df['order_date'].dt.year == 2022]

# Step 3: Count purchases per customer
customer_purchases = df_2022.groupby('customer_id').size().reset_index(name='purchase_count')

# Step 4: Categorize customers
one_time_customers = customer_purchases[customer_purchases['purchase_count'] == 1].shape[0]
repeat_customers = customer_purchases[customer_purchases['purchase_count'] > 1].shape[0]

# Step 5: Calculate ratio
ratio_repeat = repeat_customers / (one_time_customers + repeat_customers)

# Step 6: Display results (Scorecard style)
print("Customer Purchase Analysis (2022)")
print("--------------------------------")
print(f"Unique Customers (1 purchase): {one_time_customers}")
print(f"Repeat Customers (2+ purchases): {repeat_customers}")
print(f"Total Customers: {one_time_customers + repeat_customers}")
print(f"Repeat Customer Ratio: {ratio_repeat:.2%}")
