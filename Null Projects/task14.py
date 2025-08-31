import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Convert to datetime
df['order_date'] = pd.to_datetime(df['order_date'])
df['registered_date'] = pd.to_datetime(df['registered_date'])

# Step 3: Find first order date per customer
first_orders = df.groupby('customer_id')['order_date'].min().reset_index()
first_orders = first_orders.merge(df[['customer_id', 'registered_date']].drop_duplicates(),
                                  on='customer_id', how='left')

# Step 4: Calculate days between registration and first order
first_orders['days_to_first_order'] = (first_orders['order_date'] - first_orders['registered_date']).dt.days

# Step 5: Average days
avg_days = first_orders['days_to_first_order'].mean()

# Step 6: Scorecard output
print("Customer Activation Analysis")
print("-----------------------------")
print(f"Average Days to First Order: {avg_days:.2f} days")

# Step 7: Histogram visualization
plt.figure(figsize=(8,5))
plt.hist(first_orders['days_to_first_order'], bins=30, edgecolor='black')
plt.title("Distribution of Days to First Order")
plt.xlabel("Days between Registration and First Order")
plt.ylabel("Number of Customers")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
