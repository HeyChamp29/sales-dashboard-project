import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Group by category and calculate revenues
category_sales = df.groupby('category').agg(
    total_before_discount=('before_discount', 'sum'),
    total_after_discount=('after_discount', 'sum')
).reset_index()

# Step 3: Calculate discount impact
category_sales['discount_impact'] = category_sales['total_before_discount'] - category_sales['total_after_discount']

# Step 4: Plot bar chart
plt.figure(figsize=(12, 6))
bar_width = 0.35
categories = category_sales['category']
x = range(len(categories))

plt.bar(x, category_sales['total_before_discount'], width=bar_width, label='Before Discount', alpha=0.7)
plt.bar([i + bar_width for i in x], category_sales['total_after_discount'], width=bar_width, label='After Discount', alpha=0.7)

# Add discount impact line
plt.plot([i + bar_width/2 for i in x], category_sales['discount_impact'], color='red', marker='o', linestyle='--', label='Discount Impact')

plt.xticks([i + bar_width/2 for i in x], categories, rotation=45)
plt.ylabel("Revenue")
plt.title("Total Revenue vs Discount Impact by Category")
plt.legend()
plt.tight_layout()
plt.show()

# Step 5: Print data for review
print(category_sales)
