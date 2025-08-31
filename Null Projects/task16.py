import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path, parse_dates=['order_date'])

# Step 2: Extract year-month
df['year_month'] = df['order_date'].dt.to_period('M')

# Step 3: Aggregate monthly sales and discount rate
monthly_data = df.groupby('year_month').agg(
    monthly_sales=('before_discount', 'sum'),
    total_discount=('discount_amount', 'sum')
).reset_index()

# Calculate discount rate (SUM(discount_amount) / SUM(before_discount))
monthly_data['discount_rate'] = monthly_data['total_discount'] / monthly_data['monthly_sales']

# Step 4: Calculate sales growth ((current - prev)/prev)
monthly_data['sales_growth'] = monthly_data['monthly_sales'].pct_change()

# Step 5: Plot combo chart
fig, ax1 = plt.subplots(figsize=(10,6))

# Bar chart for sales growth
ax1.bar(monthly_data['year_month'].astype(str), monthly_data['sales_growth'],
        color='skyblue', label="Sales Growth (%)")
ax1.set_ylabel("Sales Growth (%)")
ax1.set_xlabel("Month")
ax1.tick_params(axis='x', rotation=45)

# Secondary axis for discount rate
ax2 = ax1.twinx()
ax2.plot(monthly_data['year_month'].astype(str), monthly_data['discount_rate'],
         color='red', marker='o', linewidth=2, label="Avg Discount Rate")
ax2.set_ylabel("Average Discount Rate")

# Title & legend
plt.title("Monthly Sales Growth vs Discount Rate")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

plt.tight_layout()
plt.show()
