import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# Step 3: Filter data for 2022
df_2022 = df[df['order_date'].dt.year == 2022].copy()

# Step 4: Extract month
df_2022['month'] = df_2022['order_date'].dt.to_period('M')

# Step 5: Calculate AOV = SUM(after_discount) / COUNT_DISTINCT(id)
aov_data = df_2022.groupby('month').agg(
    total_revenue=('after_discount', 'sum'),
    total_orders=('id', pd.Series.nunique)  # COUNT DISTINCT id
).reset_index()

aov_data['AOV'] = aov_data['total_revenue'] / aov_data['total_orders']

# Step 6: Plot AOV trend
plt.figure(figsize=(10, 6))
plt.plot(aov_data['month'].astype(str), aov_data['AOV'], marker='o', linestyle='-', color='b')

plt.title("Average Order Value (AOV) Monthly Trend - 2022")
plt.xlabel("Month")
plt.ylabel("Average Order Value (AOV)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 7: Print calculated AOV values
print(aov_data)
