# 📌 Task 2: Analyzing Sales Decrease in the "Others" Category (2021 vs 2022)

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load Dataset
file_path = "data/sales_data.csv"   # <-- Update path if needed
df = pd.read_csv(file_path)

# Step 2: Ensure order_date is datetime & extract year
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['year'] = df['order_date'].dt.year

# Step 3: Filter for "Others" category, valid orders only
others_df = df[(df['category'] == "Others") & (df['is_valid'] == 1)]

# Step 4: Create sales dataset for 2021 & 2022
sales_2021 = (
    others_df[others_df['year'] == 2021]
    .groupby("sku_name", as_index=False)["qty_ordered"].sum()
    .rename(columns={"qty_ordered": "sales_2021"})
)

sales_2022 = (
    others_df[others_df['year'] == 2022]
    .groupby("sku_name", as_index=False)["qty_ordered"].sum()
    .rename(columns={"qty_ordered": "sales_2022"})
)

# Step 5: Merge datasets
merged_sales = pd.merge(sales_2021, sales_2022, on="sku_name", how="outer").fillna(0)

# Step 6: Calculate differences & percentage change
merged_sales["difference"] = merged_sales["sales_2022"] - merged_sales["sales_2021"]
merged_sales["pct_change"] = (
    ((merged_sales["sales_2022"] - merged_sales["sales_2021"]) / merged_sales["sales_2021"])
    .replace([float("inf"), -float("inf")], 0) * 100
)

# Step 7: Classify products
def classify(change):
    if change < -10:  # more than 10% drop
        return "DOWN"
    elif change > 10:  # more than 10% increase
        return "UP"
    else:
        return "FAIR"

merged_sales["status"] = merged_sales["pct_change"].apply(classify)

# Step 8: Get Top 20 products with largest decrease
top20_decrease = merged_sales.sort_values(by="difference").head(20)

# Step 9: Display Results
print("📉 Top 20 Products with Largest Sales Decrease (Others Category, 2022 vs 2021)")
print(top20_decrease[["sku_name", "sales_2021", "sales_2022", "difference", "pct_change", "status"]])

# Step 10: Visualization (Horizontal Bar Chart)
plt.figure(figsize=(12, 7))
plt.barh(top20_decrease["sku_name"], top20_decrease["difference"], color="salmon")
plt.xlabel("Sales Difference (2022 - 2021)")
plt.ylabel("Product Name")
plt.title("Top 20 Products with Largest Sales Decrease (Others Category)")
plt.gca().invert_yaxis()
plt.show()



