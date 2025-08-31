import pandas as pd

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# Step 3: Extract month and quarter
df['month'] = df['order_date'].dt.to_period('M')
df['quarter'] = df['order_date'].dt.to_period('Q')

# Step 4: Calculate net profit column
df['net_profit'] = df['after_discount'] - df['cogs']

# Step 5: Aggregate by payment method
performance = df.groupby('payment_method').agg(
    total_sales=('before_discount', 'sum'),
    total_quantity=('qty_ordered', 'sum'),
    total_net_profit=('net_profit', 'sum')
).reset_index()

print("Sales Performance by Payment Method:")
print(performance)

# ---- Optional: Filter by a specific month or quarter ----
# Example: Filter by November 2022
month_filter = "2022-11"
performance_month = df[df['month'] == month_filter].groupby('payment_method').agg(
    total_sales=('before_discount', 'sum'),
    total_quantity=('qty_ordered', 'sum'),
    total_net_profit=('net_profit', 'sum')
).reset_index()

print(f"\nSales Performance by Payment Method for {month_filter}:")
print(performance_month)

# Example: Filter by Q4 2022
quarter_filter = "2022Q4"
performance_quarter = df[df['quarter'] == quarter_filter].groupby('payment_method').agg(
    total_sales=('before_discount', 'sum'),
    total_quantity=('qty_ordered', 'sum'),
    total_net_profit=('net_profit', 'sum')
).reset_index()

print(f"\nSales Performance by Payment Method for {quarter_filter}:")
print(performance_quarter)
