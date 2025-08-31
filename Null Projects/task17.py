import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Group by category and calculate average qty sold
avg_qty_per_category = df.groupby('category')['qty_ordered'].mean().reset_index()

# Step 3: Sort in descending order
avg_qty_per_category = avg_qty_per_category.sort_values(by='qty_ordered', ascending=False)

# Step 4: Plot bar chart
plt.figure(figsize=(10,6))
plt.bar(avg_qty_per_category['category'], avg_qty_per_category['qty_ordered'], color='skyblue')

# Add labels and title
plt.xlabel("Product Category")
plt.ylabel("Average Quantity Sold")
plt.title("Average Quantity Sold per Product by Category")
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()
