import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import warnings

warnings.filterwarnings("ignore")

# --- STEP 1: LOAD & CLEAN DATA ---
print("📊 Loading Data...")
df = pd.read_csv('india_aqi_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Focus analysis on DELHI
city_name = 'Delhi'
print(f"🔍 Analyzing data for: {city_name}")

city_df = df[df['City'] == city_name][['Date', 'AQI']].set_index('Date')

# Resample to weekly average to smooth out noise
city_df = city_df.resample('W').mean()

# --- STEP 2: EDA (Visualization) ---
plt.figure(figsize=(12, 6))
sns.lineplot(data=city_df, x=city_df.index, y='AQI', label='Historical AQI')
plt.title(f'Historical AQI Trend - {city_name} (2023-2025)')

# --- UPDATE: ADDING UNITS HERE ---
plt.ylabel('AQI Index Value (0-500 scale)')
plt.xlabel('Date')

plt.axhline(y=200, color='r', linestyle='--', label='Poor Air Quality Threshold')
plt.legend()
plt.grid(True, alpha=0.3) # Added a grid for better readability
plt.savefig('aqi_trend.png')
print("📉 Plot saved as 'aqi_trend.png'")

# --- STEP 3: FORECASTING (ARIMA) ---
print("🧠 Training ARIMA Model (This may take a moment)...")

train_size = int(len(city_df) * 0.8)
train, test = city_df[0:train_size], city_df[train_size:]

model = ARIMA(train, order=(5, 1, 0))
model_fit = model.fit()

forecast = model_fit.forecast(steps=len(test))
forecast_df = pd.DataFrame(forecast, index=test.index, columns=['Forecast'])

# Calculate Error
rmse = np.sqrt(mean_squared_error(test, forecast))
print(f"✅ Model Training Complete. RMSE Error: {rmse:.2f}")

# --- STEP 4: FUTURE PREDICTION ---
print("🔮 Forecasting next 4 weeks...")
future_steps = 4
future_forecast = model_fit.forecast(steps=len(test) + future_steps)

# Plot Forecast vs Actual
plt.figure(figsize=(12, 6))
plt.plot(train.index, train['AQI'], label='Training Data')
plt.plot(test.index, test['AQI'], label='Actual Data (Test)')
plt.plot(test.index, forecast, label='ARIMA Forecast', color='red', linestyle='--')

plt.title(f'ARIMA Model Forecast vs Actual - {city_name}')

# --- UPDATE: ADDING UNITS HERE ---
plt.ylabel('AQI Index Value (0-500 scale)')
plt.xlabel('Time Period')

plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('aqi_forecast.png')
print("📈 Forecast plot saved as 'aqi_forecast.png'")