# 📌 Task 5: Finding Products with the Largest Decrease in Sales Between Two Periods (2021 vs 2022)

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load Dataset
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Ensure order_date is datetime & extract year
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['year'] = df['order_date'].dt.year

# Step 3: Aggregate sales (qty_ordered) by product for 2021 and 2022
sales_2021 = (
    df[df['year'] == 2021]
    .groupby("sku_name", as_index=False)["qty_ordered"].sum()
    .rename(columns={"qty_ordered": "sales_2021"})
)

sales_2022 = (
    df[df['year'] == 2022]
    .groupby("sku_name", as_index=False)["qty_ordered"].sum()
    .rename(columns={"qty_ordered": "sales_2022"})
)

# Step 4: Merge datasets
merged_sales = pd.merge(sales_2021, sales_2022, on="sku_name", how="outer").fillna(0)

# Step 5: Calculate differences
merged_sales["difference"] = merged_sales["sales_2022"] - merged_sales["sales_2021"]

# Step 6: Sort and get top 10 products with largest decrease
top10_decrease = merged_sales.sort_values(by="difference").head(10)

# Step 7: Display Results
print("📉 Top 10 Products with Largest Sales Decrease (2022 vs 2021)")
print(top10_decrease[["sku_name", "sales_2021", "sales_2022", "difference"]])

# Step 8: Visualization (Bar Chart)
plt.figure(figsize=(10, 6))
plt.bar(top10_decrease["sku_name"], top10_decrease["difference"], color="red")
plt.xlabel("Product Name")
plt.ylabel("Sales Difference (2022 - 2021)")
plt.title("Top 10 Products with Largest Sales Decrease")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
