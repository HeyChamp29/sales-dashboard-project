# 📌 Task 4: Comparing Weekend and Weekday Sales in Q4 2022

import pandas as pd

# Step 1: Load Dataset
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Ensure order_date is datetime
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# Step 3: Filter for Q4 2022 (Oct, Nov, Dec 2022)
q4_df = df[(df['order_date'].dt.year == 2022) & (df['order_date'].dt.month.isin([10, 11, 12]))]

# Step 4: Extract month & day info
q4_df['month'] = q4_df['order_date'].dt.month_name()
q4_df['day_name'] = q4_df['order_date'].dt.day_name()

# Step 5: Classify as Weekend or Weekday
q4_df['day_type'] = q4_df['day_name'].apply(lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday")

# Step 6: Calculate daily sales (before_discount)
daily_sales = q4_df.groupby(['order_date', 'month', 'day_type'], as_index=False)['before_discount'].sum()

# Step 7: Average daily sales by month & day_type
monthly_avg = daily_sales.groupby(['month', 'day_type'], as_index=False)['before_discount'].mean()

# Step 8: Average sales for entire Q4 (Weekend vs Weekday)
overall_avg = daily_sales.groupby('day_type', as_index=False)['before_discount'].mean()

# Step 9: Display Results
print("📊 Average Daily Sales in Q4 2022 (Weekend vs Weekday by Month):")
print(monthly_avg)

print("\n📊 Overall Average Sales in Q4 2022 (Weekend vs Weekday):")
print(overall_avg)

# Optional: Visualization
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
for month in monthly_avg['month'].unique():
    data = monthly_avg[monthly_avg['month'] == month]
    plt.bar(data['day_type'] + " - " + month, data['before_discount'])

plt.title("Average Daily Sales (Before Discount) - Q4 2022")
plt.ylabel("Average Sales")
plt.xticks(rotation=30)
plt.show()
