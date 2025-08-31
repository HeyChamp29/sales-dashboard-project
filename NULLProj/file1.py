from sqlalchemy import create_engine
import pandas as pd
from IPython.display import display
import os
import numpy as np

engine = create_engine("mysql+pymysql://root:amanshah29@localhost/sales")


queries = {
"Question 1: During the transactions that occurred in 2021, in which month did the total transaction value (after_discount) reach its highest? Use is_valid = 1 to filter transaction data. Source table : order_detail ":
r"""
  SELECT
    DATE_FORMAT(order_date, '%%m') AS Month_ID,
    DATE_FORMAT(order_date, '%%M') AS Month,
    DATE_FORMAT(order_date, '%%Y') AS Year,
    SUM(after_discount) AS total_transaction
  FROM order_detail
  WHERE YEAR(order_date) = 2021
  AND is_valid = 1
  GROUP BY Month_ID, Month, Year
  ORDER BY total_transaction DESC;
""",


"Question: 2 During transactions in the year 2022, which category generated the highest transaction value? Use is_valid = 1 to filter transaction data. Source table : order_detail, sku_detail " :

r"""
SELECT
    DATE_FORMAT(ordet.order_date, '%%Y') AS year,
    skudet.category,
    SUM(ordet.after_discount) AS total_transaction
FROM
    order_detail AS ordet
    JOIN sku_detail AS skudet ON ordet.sku_id = skudet.id
WHERE
    ordet.is_valid = 1
    AND DATE_FORMAT(ordet.order_date, '%%Y') = '2022'
GROUP BY
    DATE_FORMAT(ordet.order_date, '%%Y'),
    skudet.category
ORDER BY
    total_transaction DESC;
""",

"Question 3: Compare the transaction values of each category in the years 2021 and 2022.Mention which categories experienced an increase and which categories experienced a decrease in transaction values from 2021 to 2022.Use is_valid = 1 to filter transaction data. Source table : order_detail, sku_detail " :

r"""
with
final_table as (
	select
		skudet.category,
        SUM(case when extract(year from ordet.order_date) = 2021 then ordet.after_discount end) as transaction_2021,
		SUM(case when extract(year from ordet.order_date) = 2022 then ordet.after_discount end) as transaction_2022
	from order_detail as ordet
    join sku_detail as skudet on ordet.sku_id = skudet.id
    where ordet.is_valid = 1
    group by 1
    order by 1
    )
select *, (transaction_2022 - transaction_2021) as delta,
case when transaction_2022>transaction_2021 then 'INCREASE' else 'DECREASE' end as remark
from final_table;

""",

"Question 4: Display the top 5 most popular payment methods used during 2022 (based on total unique orders). Use is_valid = 1 to filter transaction data.Source table : order_detail, payment_detail ":

r"""
SELECT
    paydet.payment_method,
    DATE_FORMAT(ordet.order_date, '%%Y') AS year,
    COUNT(DISTINCT ordet.id) AS freq
FROM
    order_detail AS ordet
JOIN
    payment_detail AS paydet ON ordet.payment_id = paydet.id
WHERE
    ordet.is_valid = 1 
    AND YEAR(ordet.order_date) = 2022
GROUP BY
    paydet.payment_method,
    DATE_FORMAT(ordet.order_date, '%%Y')
ORDER BY
    freq DESC
LIMIT 5;
""",


"Question 5: Sort these 5 products based on their transaction values.1. Samsung, 2. Apple, 3. Sony, 4. Huawei, 5. Lenovo.Use is_valid = 1 to filter transaction data.":
r"""
WITH final_table AS (
    SELECT
        CASE
            WHEN LOWER(skudet.sku_name) LIKE '%%samsung%%' THEN 'Samsung'
            WHEN LOWER(skudet.sku_name) LIKE '%%apple%%' 
                 OR LOWER(skudet.sku_name) LIKE '%%iphone%%' 
                 OR LOWER(skudet.sku_name) LIKE '%%macbook%%' THEN 'Apple'
            WHEN LOWER(skudet.sku_name) LIKE '%%sony%%' THEN 'Sony'
            WHEN LOWER(skudet.sku_name) LIKE '%%huawei%%' THEN 'Huawei'
            WHEN LOWER(skudet.sku_name) LIKE '%%lenovo%%' THEN 'Lenovo'
        END AS product_brand,
        SUM(ordet.after_discount) AS total_transaction
    FROM
        order_detail AS ordet
    JOIN
        sku_detail AS skudet ON ordet.sku_id = skudet.id
    WHERE
        ordet.is_valid = 1
    GROUP BY
        product_brand
)
SELECT *
FROM final_table
WHERE product_brand IS NOT NULL
ORDER BY total_transaction DESC;
"""

}



# connect to database

try :
    print("Connection established")

    # Execute each query and display results

    for question, query in queries.items():
         print(f"\n---{question}---")
         df = pd.read_sql_query(query, engine)
         display(df)

except Exception as e :
     print(f"An error occurred: {e}")
finally:
        engine.dispose()
        print("Connection closed")

# Folder Path to save CSV Files

output_folder = r"/Users/amanjayeshshah/PyCharmMiscProject/NULLProj"
os.makedirs(output_folder, exist_ok=True)


# List of tables to export

tables = ["order_detail", "sku_detail", "payment_detail","customer_detail"]

try:
    print("Database Connection established")


    for table in tables :
        print(f"Exporting table : {table}")

    # SQL Query to fetch all data from the table

        query = f"SELECT * FROM {table}"

    # Read Table data into a DataFrame

        df = pd.read_sql_query(query, engine)

    # Save the dataframe to a CSV File


        df.to_csv(f"{table}.csv", index=False)


except Exception as e :
    print(f"An error occurred: {e}")
finally:
    engine.dispose()
    print("Connection closed")


import pandas as pd

# Load CSVs
df_od = pd.read_csv("order_detail.csv")
df_sd = pd.read_csv("sku_detail.csv")
df_pd = pd.read_csv("payment_detail.csv")
df_cd = pd.read_csv("customer_detail.csv")

# ✅ Rename columns so they don't conflict (id → proper key name)
df_sd.rename(columns={'id': 'sku_id'}, inplace=True)
df_cd.rename(columns={'id': 'customer_id'}, inplace=True)
df_pd.rename(columns={'id': 'payment_id'}, inplace=True)

# ✅ Merge step by step (left join keeps all order_detail rows)
df = (
    df_od
    .merge(df_sd, how="left", on="sku_id")       # Join order_detail ↔ sku_detail
    .merge(df_cd, how="left", on="customer_id")  # Join with customer_detail
    .merge(df_pd, how="left", on="payment_id")   # Join with payment_detail
)

df.info()

print(df_pd.columns)

print(df_od. columns)


# Ensure both columns have the same data type before merging
df_pd[ 'payment_id'] = df_pd[ 'payment_id'] .astype(str)
df_od['id'] = df_od[ 'id'].astype(str)
# Convert to string
# Convert to string
# Merge order_detail with payment_detail without renaming columns
df_sample = pd.merge(df_pd, df_od, how='left', left_on='payment_id', right_on='id')

# Display info about the resulting DataFrame
df_sample.info()


for x in ['order_date', 'registered_date']:
    df[x] = pd.to_datetime(df[x])

df.info()



"Question 1 : Dear Data Analyst,As part of our Year-End Festival competition, the company plans to award prizes to our top customers. To facilitate this, the Marketing Team requires an analysis to estimate the prizes for the winners. Specifically, we need data on the TOP 5 Products in the Mobiles & Tablets Category for the year 2022, ranked by the highest sales quantities (where valid = 1).we would appreciatefit if you could compile and share this information with us before the end of this month to ensure we meet our planning deadlines.Thank you for your continued support and collaboration.Best regards,"
"Marketing Teameting Team "

top_5_prod = pd.DataFrame(\
# filter the columns as needed
df[(df['category'] == 'Mobiles & Tablets') & (df['is_valid'] == 1) & (df['order_date'].dt.year == 2022)] \
    # aggregate using groupby method
    .groupby(by=['sku_name', 'category'])['qty_ordered'].sum() \
    # reset the index to convert result into dataframe
    .reset_index(name='qty_ordered') \
    # sort the value from the largest to the Lowest
    .sort_values(by='qty_ordered', ascending=False) \
    # select top 5 row
     .head(5).reset_index(drop=True)
)
print(top_5_prod)



# plot
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
#
# ax = top_5_prod.plot(
#     x='sku_name',
#     y='qty_ordered',
#     kind='bar',
#     figsize=(12, 7),
#     rot=0,
#     grid=True,
#     legend=False,
#     color="skyblue"   # optional, for nicer look
# )
#
# # Add labels and title
# plt.xlabel("Product Name")
# plt.ylabel("Quantity Ordered")
# plt.title("TOP 5 Products in Mobiles & Tablets (2022)")
#
# # Show values on top of bars
# for p in ax.patches:
#     ax.annotate(str(p.get_height()),
#                 (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='bottom')
#
# plt.tight_layout()
# plt.show()
#
#
# # Sort ascending so highest appears at bottom of horizontal bar chart
# top_5_prod.sort_values(by='qty_ordered', ascending=True, inplace=True)
#
# # Plot horizontal bar chart
# sns.set()
# ax = top_5_prod.plot(
#     x='sku_name',
#     y='qty_ordered',
#     kind='barh',
#     figsize=(12, 7),
#     grid=True,
#     legend=False,
#     color="skyblue"
# )
#
#
# # Sort ascending so highest appears at bottom of horizontal bar chart
# top_5_prod.sort_values(by='qty_ordered', ascending=True, inplace=True)
#
# # Plot horizontal bar chart
# sns.set()
# ax = top_5_prod.plot(
#     x='sku_name',
#     y='qty_ordered',
#     kind='barh',
#     figsize=(12, 7),
#     grid=True,
#     legend=False,
#     color="skyblue"
# )
#
# # Labels and title
# plt.xlabel("Quantity")
# plt.ylabel("Product Name")
# plt.title("TOP 5 Products in Mobiles & Tablets (2022)")
#
# # Show values on bars
# for p in ax.patches:
#     ax.annotate(str(p.get_width()),
#                 (p.get_width(), p.get_y() + p.get_height() / 2),
#                 ha='left', va='center')
#
# plt.tight_layout()
# plt.show()


"Dear Data Analyst,"
"Following a recent discussion between the Warehouse and Marketing Teams, we have identified a notable surplus in stock for products in the 'Others' category as of the end of 2022."
"We kindly request your assistance in analyzing the sales data for this category for 2021, specifically focusing on sales quantity. We suspect there has been a decline in sales quantity in 2022 compared to 2021. (Please also include data for the 15th category.)"
"If a decrease in sales quantity for the 'Others' fitegory is confirmed, we would appreciate it if you could provide details of the top 20 products that experienced the largest decrease in sales between 2022 and 2021. This information will support our discussion in the upcoming meeting."
"Please share the requested data within 4 days. We sincerely appreciate your assistance and cooperation."
"Best regards, Warehouse Team"

#
# # 1. Build category-level data for 2021
# cat_data_2021 = (
#     df[(df['is_valid'] == 1) & (df['order_date'].dt.year == 2021)]
#     .groupby('category', as_index=False)['qty_ordered']
#     .sum()
#     .rename(columns={'qty_ordered': 'qty_ordered_2021'})
# )
#
# # 2. Build category-level data for 2022
# cat_data_2022 = (
#     df[(df['is_valid'] == 1) & (df['order_date'].dt.year == 2022)]
#     .groupby('category', as_index=False)['qty_ordered']
#     .sum()
#     .rename(columns={'qty_ordered': 'qty_ordered_2022'})
# )
#
# # 3. Merge both years into one DataFrame
# cat_data_2021_2022 = pd.merge(cat_data_2021, cat_data_2022, on='category', how='outer').fillna(0)
#
# # 4. Add growth and growth percentage
# cat_data_2021_2022['qty_growth'] = cat_data_2021_2022['qty_ordered_2022'] - cat_data_2021_2022['qty_ordered_2021']
#
# cat_data_2021_2022['growth_percentage'] = cat_data_2021_2022.apply(
#     lambda x: round((x['qty_growth'] / x['qty_ordered_2021'] * 100), 2) if x['qty_ordered_2021'] > 0 else 0,
#     axis=1
# )
#
# # 5. Add remark column
# def updown_check(delta):
#     if delta < 0:
#         return 'DOWN'
#     elif delta == 0:
#         return 'FAIR'
#     else:
#         return 'UP'
#
# cat_data_2021_2022['remark'] = cat_data_2021_2022['qty_growth'].apply(updown_check)
#
# # 6. Sort for better readability
# cat_data_2021_2022.sort_values(by='qty_growth', ascending=True, inplace=True)
# cat_data_2021_2022.reset_index(drop=True, inplace=True)
#
# # show all rows and columns without dots
# pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", None)
#
# print(cat_data_2021_2022)
#
#
# # # sort before plot
# # cat_data_2021_2022.sort_values(by='qty_growth', ascending=False, inplace=True)
# #
# # # plot to show qty_ordered_2021 and qty_ordered_2022, horizontal bar
# # sns.set()
# #
# # cat_data_2021_2022.plot(
# #     x='category',
# #     y=['qty_ordered_2021', 'qty_ordered_2022'],
# #     kind='barh',
# #     figsize=(10, 8)
# # )
# #
# # plt.title('Quantity Growth Per Category 2022 vs 2021')
# # plt.ylabel('Category')
# # plt.xlabel('Quantity')
# # plt.show()
#
# # Sort by growth percentage descending
# cat_data_2021_2022.sort_values(by='growth_percentage', ascending=False, inplace=True)
#
# # Plot horizontal bar for growth_percentage
# sns.set()
# ax = cat_data_2021_2022.plot(
#     x='category',
#     y='growth_percentage',
#     kind='barh',
#     figsize=(10, 8),
#     color='skyblue',
#     legend=False
# )
#
# # Labels and title
# plt.title('Growth Percentage Per Category 2022 vs 2021')
# plt.xlabel('Growth Percentage (%)')
# plt.ylabel('Category')
#
# # Annotate values on bars
# for p in ax.patches:
#     ax.annotate(f"{p.get_width():.2f}%",
#                 (p.get_width() + 1, p.get_y() + p.get_height()/2),
#                 ha='left', va='center')
#
# plt.tight_layout()
# plt.show()


# # 1. Data for category = 'Others', year 2022
# others_2022 = (
#     df[(df['category'] == 'Others') & (df['is_valid'] == 1) & (df['order_date'].dt.year == 2022)]
#     .groupby(['sku_name', 'category'], as_index=False)['qty_ordered']
#     .sum()
#     .rename(columns={'qty_ordered': 'qty_ordered_2022'})
# )
#
# # 2. Data for category = 'Others', year 2021
# others_2021 = (
#     df[(df['category'] == 'Others') & (df['is_valid'] == 1) & (df['order_date'].dt.year == 2021)]
#     .groupby(['sku_name', 'category'], as_index=False)['qty_ordered']
#     .sum()
#     .rename(columns={'qty_ordered': 'qty_ordered_2021'})
# )
#
# # 3. Merge 2021 and 2022 data
# others_2021_2022 = pd.merge(
#     others_2021,
#     others_2022[['sku_name', 'qty_ordered_2022']],
#     how='outer',
#     on='sku_name'
# ).fillna(0)
#
# # 4. Add growth and growth percentage
# others_2021_2022['qty_growth'] = others_2021_2022['qty_ordered_2022'] - others_2021_2022['qty_ordered_2021']
#
# import numpy as np  # make sure numpy is imported
# others_2021_2022['growth_percentage'] = (
#     (others_2021_2022['qty_growth'] / others_2021_2022['qty_ordered_2021'].replace(0, np.nan)) * 100
# ).round(2)
#
# # 5. Add remark column
# def updown_check(delta):
#     if delta < 0:
#         return 'DOWN'
#     elif delta == 0:
#         return 'FAIR'
#     else:
#         return 'UP'
#
# others_2021_2022['remark'] = others_2021_2022['qty_growth'].apply(updown_check)
#
# # 6. Sort by growth
# others_2021_2022.sort_values(by='qty_growth', ascending=False, inplace=True)
# others_2021_2022.reset_index(drop=True, inplace=True)
#
# print(others_2021_2022)
#
# # Fill NaN in 'category' column with "Others"
# others_2021_2022['category'] = others_2021_2022['category'].fillna('Others')
#
# # Fill the rest of NaN values with 0
# others_2021_2022.fillna(0, inplace=True)
#
# # Show the data
# print(others_2021_2022)
#
# # 1. Add column delta_2022_2021
# others_2021_2022['delta_2022_2021'] = others_2021_2022['qty_ordered_2022'] - others_2021_2022['qty_ordered_2021']
#
# # 2. Add column remark using function updown_check
# others_2021_2022['remark'] = others_2021_2022['delta_2022_2021'].apply(updown_check)
#
# # 3. Sort values from smallest to largest
# others_2021_2022.sort_values(by='delta_2022_2021', ascending=True, inplace=True)
#
# # 4. Reset index
# others_2021_2022.reset_index(drop=True, inplace=True)
#
# # 5. Show the data
# print(others_2021_2022)
#
#
#
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# # Choose top 20 products (smallest delta)
# others_2021_2022 = others_2021_2022.head(20)
#
# # Sort descending to show largest decrease at top
# others_2021_2022.sort_values(by='delta_2022_2021', ascending=False, inplace=True)
#
# # Set seaborn style
# sns.set(style="whitegrid")
#
# # Plot horizontal bar chart
# ax = others_2021_2022.plot(
#     x='sku_name',
#     y='delta_2022_2021',
#     kind='barh',
#     figsize=(10, 8),
#     color='salmon',
#     legend=False
# )
#
# # Add labels and title
# plt.title('Top Decreased Products 2022 vs 2021 - "Others" Category')
# plt.xlabel('Delta 2022_2021')
# plt.ylabel('Product Name')
#
# # Annotate values on bars
# for p in ax.patches:
#     ax.annotate(f"{p.get_width():.0f}",
#                 (p.get_width() + 1, p.get_y() + p.get_height()/2),
#                 ha='left', va='center')
#
# plt.tight_layout()
# plt.show()
#



"Que 3 :Dear Data Analyst,"
"As we prepare for the company's upcoming anniversary in two months, the Digital Marketing Team plans to share promotional information with customers by the end of this"
"month. To support this initiative, we require data on customers who completed the check-out process but have not yet made a payment (is-gross = 1) during the year 2022."
"Specifically, we need the Customer IDs and their Registered Dates."
"We kindly request your assistance in compiling and delivering this data to the Digital Marketing Team before the month's end. Your support in this matter is greatly appreciated."
"Best regards, Digital Marketing Team"


# Filter as requested
# cs_gross_data = df.loc[
#     :, ['customer_id', 'registered_date']  # correct column name
# ][
#     (df['is_gross'] == 1) &
#     (df['is_valid'] == 0) &
#     (df['is_net'] == 0) &
#     (df['order_date'].dt.year == 2022)
# ]
#
# # Show the data
# print(cs_gross_data)
#
#
# # Function to validate duplicates
# def check_customerid(x):
#     unique_customerid = len(x['customer_id'].unique().tolist())
#     rows_count = len(x.index)
#     return [unique_customerid, rows_count]
#
# # Run validation before removing duplicates
# test = check_customerid(cs_gross_data)
# print('Data Before :', test)
#
# # Check for duplicates
# if test[0] == test[1]:
#     print('There is no duplicated data.')
# else:
#     print('There is duplicated data.')
#     # Remove duplicates
#     cs_gross_data.drop_duplicates(inplace=True)
#     print('Data After removing duplicates:', check_customerid(cs_gross_data))
#
# # Reset index and show final data
# cs_gross_data.reset_index(drop=True, inplace=True)
# print(cs_gross_data)



"Que : 4  Dear Data Analyst,"
"Between October and December 2022, we ran promotional campaigns every Saturday and Sunday. To evaluate their effectiveness, we would like your assistance in analyzing the following:"
"The average daily sales (before_discount) for weekends (Saturday and Sunday) compared to weekdays (Monday-Friday) for each month during this period. Please specify whether sales increased during weekends for each month."
"The average daily sales (before _discount) for weekends versus weekdays across the entire three-month period"
"We kindly request the data to be shared with us by the end of next week. Thank you for your continued support."
"Best regards, Campaign Team"

# Add month_id, month_name, day_name, and year columns
# df['month_id'] = df['order_date'].dt.month
# df['month_name'] = df['order_date'].dt.month_name()
# df['day_name'] = df['order_date'].dt.day_name()
# df['year'] = df['order_date'].dt.year
#
# # Show first few rows
# print(" ")
# print(df.head())
#
#
# # Create dataframe for weekends data October-December 2022
# data_weekends = (
#     df[
#         (df['is_valid'] == 1) &
#         (df['day_name'].isin(['Saturday', 'Sunday'])) &
#         (df['month_id'] >= 10) &
#         (df['year'] == 2022)
#     ]
#     .groupby(['month_id', 'month_name', 'year'], as_index=False)['before_discount']
#     .mean()
#     .round(2)
#     .rename(columns={'before_discount': 'avg_sales_weekends'})
#     .sort_values(by='month_id', ascending=True)
# )
#
# # Create dataframe for weekdays data October-December 2022
# data_weekdays = (
#     df[
#         (df['is_valid'] == 1) &
#         (df['day_name'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])) &
#         (df['month_id'] >= 10) &
#         (df['year'] == 2022)
#     ]
#     .groupby(['month_id', 'month_name', 'year'], as_index=False)['before_discount']
#     .mean()
#     .round(2)
#     .rename(columns={'before_discount': 'avg_sales_weekdays'})
#     .sort_values(by='month_id', ascending=True)
# )
#
# # Merge weekdays and weekends data
# data_weekdays_weekends = pd.merge(
#     data_weekdays,
#     data_weekends,
#     on=['month_id', 'month_name', 'year'],
#     how='outer'
# )
#
# # Show the merged data
# print(data_weekdays_weekends)
#
#
# # Set seaborn style
# sns.set(style="whitegrid")
#
# # Plot the data
# ax = data_weekdays_weekends.plot(
#     x='month_name',
#     y=['avg_sales_weekdays', 'avg_sales_weekends'],
#     kind='bar',
#     figsize=(12, 10),
#     grid=True,
#     rot=50,
#     xlabel='Month Name',
#     ylabel='Average Sales',
#     table=False,
#     secondary_y=False
# )
#
# plt.title('Average Sales: Weekdays vs Weekends (Oct-Dec 2022)')
# plt.tight_layout()
# plt.show()
#
#
#
# # Filter dataframe for weekends, October-December 2022
# data_weekends_all = df[
#     (df['is_valid'] == 1) &
#     (df['day_name'].isin(['Saturday', 'Sunday'])) &
#     (df['month_id'] >= 10) &
#     (df['year'] == 2022)
# ]
#
# # Filter dataframe for weekdays, October-December 2022
# data_weekdays_all = df[
#     (df['is_valid'] == 1) &
#     (df['day_name'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])) &
#     (df['month_id'] >= 10) &
#     (df['year'] == 2022)
# ]
#
# # Create dictionary with comparison metrics
# all_month_avg_compare = {
#     'Period': 'Total 3 months',
#     'Avg Weekdays Sales': round(data_weekdays_all['before_discount'].mean(), 2),
#     'Avg Weekends Sales': round(data_weekends_all['before_discount'].mean(), 2),
#     'Diff (Value)': round(
#         data_weekends_all['before_discount'].mean() - data_weekdays_all['before_discount'].mean(), 2
#     ),
#     'Diff (%)': round(
#         ((data_weekends_all['before_discount'].mean() - data_weekdays_all['before_discount'].mean())
#          / data_weekdays_all['before_discount'].mean()) * 100, 2
#     )
# }
#
# # Create DataFrame from dictionary
# compare_avg_weekends_weekdays = pd.DataFrame([all_month_avg_compare])
#
# # Show the data
# print(compare_avg_weekends_weekdays)
#
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# # Set seaborn style
# sns.set(style="whitegrid")
#
# # Plot Avg Weekdays vs Avg Weekends
# ax = compare_avg_weekends_weekdays.plot(
#     x='Period',
#     y=['Avg Weekdays Sales', 'Avg Weekends Sales'],
#     kind='bar',
#     figsize=(12, 10),
#     grid=True,
#     rot=0,
#     ylabel='Average Sales',
#     table=False,
#     secondary_y=False
# )
#
# plt.title('Average Sales: Weekdays vs Weekends (Oct-Dec 2022)')
# plt.xlabel('Period')
# plt.tight_layout()
# plt.show()



# Save CSV in the same folder where file1.py is located
df.to_csv("finaldataset.csv", index=False)

print("File successfully saved next to file1.py")


import os

# Save CSV next to file1.py
file_name = "finaldataset.csv"
df.to_csv(file_name, index=False)

# Get absolute path of the saved file
abs_path = os.path.abspath(file_name)

print(f"File successfully saved at: {abs_path}")


import os

file_name = "test.csv"

# Just create a dummy CSV without needing df
import pandas as pd
pd.DataFrame({"a": [1, 2, 3]}).to_csv(file_name, index=False)

abs_path = os.path.abspath(file_name)
print("✅ File successfully saved at:", abs_path)



