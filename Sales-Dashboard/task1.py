"""
Task 1: Top 5 Products by Sales in 2022 for 'Mobiles & Tablets'

Requirements:
- Filter data for category = 'Mobiles & Tablets'
- Year = 2022
- is_valid = 1
- Group by product (sku_name) and sum qty_ordered
- Rank products by sales quantity (descending)
- Display top 5 products
- Plot horizontal bar chart
"""

import pandas as pd
import matplotlib.pyplot as plt
import os



# Step 1: Load dataset
file_path = os.path.join("data", "sales_data.csv")  # adjust if needed
df = pd.read_csv(file_path)

# Step 2: Convert date and extract year
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['year'] = df['order_date'].dt.year

# Step 3: Filter dataset
filtered_df = df[
    (df['category'] == "Mobiles & Tablets") &
    (df['year'] == 2022) &
    (df['is_valid'] == 1)
]

# Step 4: Group and aggregate
grouped_df = (
    filtered_df.groupby(['sku_name'], as_index=False)
    .agg({'qty_ordered': 'sum'})
)

# Step 5: Sort and take top 5
top5_products = grouped_df.sort_values(by="qty_ordered", ascending=False).head(5)

# Step 6: Print results
print("✅ Top 5 Products by Sales Quantity (Mobiles & Tablets, 2022, Valid Orders)")
print(top5_products)

# Step 7: Visualization
plt.figure(figsize=(10, 6))
bars = plt.barh(top5_products['sku_name'], top5_products['qty_ordered'], color="skyblue")
plt.xlabel("Total Quantity Ordered")
plt.ylabel("Product Name")
plt.title("Top 5 Mobiles & Tablets Products (2022, Valid Orders)")
plt.gca().invert_yaxis()  # highest first

# Add labels
for bar in bars:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
             str(bar.get_width()), va='center')

# Save chart to output folder
os.makedirs("output", exist_ok=True)
plt.savefig("output/chart_task1.png", dpi=300, bbox_inches="tight")
plt.show()




