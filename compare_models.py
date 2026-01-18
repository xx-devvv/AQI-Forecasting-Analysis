import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
import warnings

warnings.filterwarnings("ignore")

# --- 1. Load Data ---
print("📊 Loading Data...")
df = pd.read_csv('india_aqi_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
city_df = df[df['City'] == 'Delhi'][['Date', 'AQI']].sort_values('Date')

# Resample to Weekly for stability
data = city_df.set_index('Date').resample('W').mean().reset_index()

# Split Train/Test
train_size = int(len(data) * 0.8)
train, test = data.iloc[:train_size], data.iloc[train_size:]

# --- 2. Model A: ARIMA (Trend Focused) ---
print("🤖 Training ARIMA (Standard Model)...")
arima_model = ARIMA(train['AQI'], order=(5,1,0))
arima_fit = arima_model.fit()
arima_pred = arima_fit.forecast(steps=len(test))
arima_rmse = np.sqrt(mean_squared_error(test['AQI'], arima_pred))

# --- 3. Model B: Holt-Winters (Seasonal Focused) ---
print("🔮 Training Holt-Winters (Seasonal Model)...")

# FIX: We changed seasonal_periods to 12 (Quarterly) to fit the dataset size
# We also used initialization_method='estimated' to handle short data better
hw_model = ExponentialSmoothing(
    train['AQI'],
    seasonal_periods=12,  # Changed from 52 to 12 (Quarterly pattern)
    trend='add',
    seasonal='add',
    initialization_method='estimated'
).fit()

hw_pred = hw_model.forecast(steps=len(test))
hw_rmse = np.sqrt(mean_squared_error(test['AQI'], hw_pred))

# --- 4. Comparison & Visualization ---
print(f"\n🏆 RESULTS:")
print(f"ARIMA RMSE (Trend):      {arima_rmse:.2f}")
print(f"Seasonal Model RMSE:     {hw_rmse:.2f}")

if hw_rmse < arima_rmse:
    winner = "Seasonal Model"
    print("✅ Best Model: Seasonal (Holt-Winters) - Captured the spikes better.")
else:
    winner = "ARIMA"
    print("✅ Best Model: ARIMA - Better at following recent trends.")

plt.figure(figsize=(14, 7))
plt.plot(train['Date'], train['AQI'], label='Training Data', color='gray', alpha=0.5)
plt.plot(test['Date'], test['AQI'], label='Actual Data', color='black', linewidth=2)

# Plot ARIMA
plt.plot(test['Date'], arima_pred, label=f'ARIMA (RMSE: {arima_rmse:.0f})', linestyle='--', color='red')

# Plot Seasonal Model
plt.plot(test['Date'], hw_pred, label=f'Seasonal Model (RMSE: {hw_rmse:.0f})', linestyle='-', color='blue')

plt.title(f'Model Comparison: ARIMA vs Seasonal Holt-Winters (Winner: {winner})')
plt.ylabel('AQI Index Value')
plt.xlabel('Date')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('model_comparison.png')
print("📉 Comparison graph saved as 'model_comparison.png'")