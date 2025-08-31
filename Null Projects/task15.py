import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Create discount categories
def categorize_discount(x):
    if x == 0:
        return "No Discount"
    elif x < 10:
        return "Low Discount"
    elif 10 <= x <= 20:
        return "Medium Discount"
    else:
        return "High Discount"

df['discount_category'] = df['discount_amount'].apply(categorize_discount)

# Step 3: Aggregate sales by discount category
sales_by_discount = df.groupby('discount_category')['before_discount'].sum().reset_index()

# Step 4: Sort categories in logical order
category_order = ["No Discount", "Low Discount", "Medium Discount", "High Discount"]
sales_by_discount['discount_category'] = pd.Categorical(sales_by_discount['discount_category'],
                                                        categories=category_order, ordered=True)
sales_by_discount = sales_by_discount.sort_values('discount_category')

# Step 5: Plot bar chart
plt.figure(figsize=(8,6))
plt.bar(sales_by_discount['discount_category'], sales_by_discount['before_discount'], color="skyblue", edgecolor="black")
plt.title("Sales Breakdown by Discount Range")
plt.xlabel("Discount Category")
plt.ylabel("Total Sales (Before Discount)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
