import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Extract year from order_date (if not already available)
df['order_date'] = pd.to_datetime(df['order_date'])
df['year'] = df['order_date'].dt.year

# Step 3: Calculate net profit
df['net_profit'] = df['after_discount'] - df['cogs']

# -------- OPTIONAL: Apply slicer (filter by year, e.g., 2022) --------
selected_year = 2022   # 👈 change this to test different years
df_filtered = df[df['year'] == selected_year]

# Step 4: Aggregate net profit by category
category_profit = df_filtered.groupby('category').agg(
    total_net_profit=('net_profit', 'sum')
).reset_index()

# Step 5: Sort categories by net profit
category_profit = category_profit.sort_values(by='total_net_profit', ascending=False)

print("Net Profit by Category (", selected_year, "):")
print(category_profit)

# Step 6: Plot bar chart
plt.figure(figsize=(10,6))
plt.bar(category_profit['category'], category_profit['total_net_profit'], color='teal')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Total Net Profit")
plt.title(f"Product Category Performance by Net Profit ({selected_year})")
plt.show()
