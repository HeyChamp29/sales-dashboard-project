import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "/Users/amanjayeshshah/PyCharmMiscProject/Null Projects/Data/sales_data.csv"
df = pd.read_csv(file_path)

# Step 2: Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# Step 3: Aggregate monthly sales
df['year_month'] = df['order_date'].dt.to_period("M")
monthly_sales = df.groupby('year_month')['qty_ordered'].sum().to_timestamp()

# Step 4: Train on 2022 data
train = monthly_sales['2022-01':'2022-12']

# Step 5: Build Holt-Winters model (trend only)
model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal=None
).fit()

# Step 6: Forecast next 3 months (Q2 2023)
forecast = model.forecast(3)

# Step 7: Evaluate accuracy on training set (backtest)
y_pred = model.fittedvalues
mae = mean_absolute_error(train, y_pred)
rmse = np.sqrt(mean_squared_error(train, y_pred))

print("📊 Forecast for Q2 2023 (Monthly Sales):")
print(forecast)
print(f"\nModel Accuracy on Training Data - MAE: {mae:.2f}, RMSE: {rmse:.2f}")

# Step 8: Visualization
plt.figure(figsize=(10, 6))
plt.plot(train.index, train, label="Historical Sales (2022)")
plt.plot(y_pred.index, y_pred, label="Fitted Values", linestyle="--")
plt.plot(forecast.index, forecast, label="Forecast (Q2 2023)", color="red", marker="o")
plt.title("Sales Forecast for Q2 2023 (Trend Model)")
plt.xlabel("Date")
plt.ylabel("Sales (qty_ordered)")
plt.legend()
plt.show()
