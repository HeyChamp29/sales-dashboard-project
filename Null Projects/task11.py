import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Calculate net profit
df['net_profit'] = df['after_discount'] - df['cogs']

# Step 3: Aggregate net profit per customer
customer_profit = df.groupby('customer_id').agg(
    total_net_profit=('net_profit', 'sum')
).reset_index()

# Step 4: Categorize into segments
def categorize_profit(x):
    if x < 100:
        return "Low"
    elif 100 <= x <= 500:
        return "Medium"
    else:
        return "High"

customer_profit['segment'] = customer_profit['total_net_profit'].apply(categorize_profit)

# Step 5: Count customers per segment
segment_distribution = customer_profit['segment'].value_counts().reset_index()
segment_distribution.columns = ['Segment', 'Customer_Count']

print("Customer Segment Distribution:")
print(segment_distribution)

# Step 6: Pie chart
plt.figure(figsize=(6,6))
plt.pie(segment_distribution['Customer_Count'],
        labels=segment_distribution['Segment'],
        autopct='%1.1f%%',
        startangle=140,
        explode=(0.05, 0.05, 0.05),
        shadow=True)

plt.title("Customer Distribution by Net Profit Segment")
plt.show()
