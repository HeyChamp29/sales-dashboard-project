# 📌 Task 6: Comparing Sales Trends for Multiple Categories in 2022

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load Dataset
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Ensure order_date is datetime & extract year/month
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.to_period("M")  # year-month format

# Step 3: Filter for 2022
df_2022 = df[df['year'] == 2022]

# Step 4: Aggregate sales by category & month
category_trends = (
    df_2022.groupby(["month", "category"], as_index=False)["qty_ordered"]
    .sum()
    .sort_values(by="month")
)

# Step 5: Pivot for plotting (months as x-axis, categories as lines)
pivot_trends = category_trends.pivot(index="month", columns="category", values="qty_ordered").fillna(0)

# Step 6: Plot sales trends
plt.figure(figsize=(12, 7))
for category in pivot_trends.columns:
    plt.plot(pivot_trends.index.astype(str), pivot_trends[category], marker="o", label=category)

plt.xlabel("Month (2022)")
plt.ylabel("Total Sales (qty_ordered)")
plt.title("📈 Sales Trends by Category in 2022")
plt.legend(title="Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 7: Insights (calculate growth from Jan to Dec)
growth = {}
for category in pivot_trends.columns:
    first_val = pivot_trends[category].iloc[0]
    last_val = pivot_trends[category].iloc[-1]
    growth[category] = (last_val - first_val)

print("\n📊 Category Growth from Jan to Dec 2022:")
for cat, val in sorted(growth.items(), key=lambda x: x[1], reverse=True):
    status = "📈 Growth" if val > 0 else "📉 Decline"
    print(f"{cat}: {val} ({status})")

best_category = max(growth, key=growth.get)
print(f"\n🏆 Best Performing Category in 2022: {best_category}")
