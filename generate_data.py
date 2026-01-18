import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration
cities = ['Delhi', 'Mumbai', 'Kolkata', 'Bengaluru']
start_date = datetime(2023, 1, 1)
days = 1095  # 3 Years of data
data = []

print("🏭 Generating synthetic Air Quality Data...")

for city in cities:
    # Base pollution levels (Delhi is highest, Bengaluru lowest)
    base_aqi = {'Delhi': 250, 'Mumbai': 120, 'Kolkata': 180, 'Bengaluru': 90}[city]

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        month = current_date.month

        # Seasonal Trend: Winter (Nov-Jan) is worse, Monsoon (Jul-Sep) is better
        if month in [11, 12, 1]:  # Winter
            season_factor = 1.5
        elif month in [7, 8, 9]:  # Monsoon
            season_factor = 0.6
        else:
            season_factor = 1.0

        # Random daily fluctuation
        daily_noise = np.random.normal(0, 20)

        # Calculate Pollutants (correlated with AQI)
        aqi = max(50, (base_aqi * season_factor) + daily_noise)
        pm25 = aqi * 0.6  # PM2.5 usually drives AQI
        pm10 = aqi * 0.8
        no2 = aqi * 0.3

        data.append([city, current_date, round(pm25, 2), round(pm10, 2), round(no2, 2), int(aqi)])

# Create DataFrame
df = pd.DataFrame(data, columns=['City', 'Date', 'PM2.5', 'PM10', 'NO2', 'AQI'])

# Save to CSV
df.to_csv('india_aqi_data.csv', index=False)
print("✅ Success! 'india_aqi_data.csv' has been created.")