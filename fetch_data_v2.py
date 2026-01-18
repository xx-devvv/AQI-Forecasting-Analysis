import requests
import pandas as pd

# --- STEP 1: SETUP FOR OPEN-METEO API ---
print("📡 Connecting to Open-Meteo Historical Air Quality API...")

# Delhi Coordinates
LAT = 28.6139
LON = 77.2090

# URL for Historical Air Quality (Reanalysis data is best for training models)
url = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": LAT,
    "longitude": LON,
    "hourly": ["pm10", "pm2_5", "nitrogen_dioxide"],  # Parameters we need
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "timezone": "Asia/Kolkata"
}

# --- STEP 2: FETCH & PROCESS ---
try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract Hourly Data
    hourly = data['hourly']

    # Create DataFrame
    df = pd.DataFrame({
        'Date': pd.to_datetime(hourly['time']),
        'PM10': hourly['pm10'],
        'PM2.5': hourly['pm2_5'],
        'NO2': hourly['nitrogen_dioxide']
    })

    # Add City Name
    df['City'] = 'Delhi'


    # --- STEP 3: CALCULATE PROXY AQI ---
    # Simplified formula for project demo purposes
    def calculate_aqi(pm25):
        if pm25 <= 30:
            return pm25 * 1.6
        elif pm25 <= 60:
            return 50 + (pm25 - 30) * 1.6
        elif pm25 <= 90:
            return 100 + (pm25 - 60) * 3.3
        elif pm25 <= 120:
            return 200 + (pm25 - 90) * 3.3
        else:
            return 300 + (pm25 - 120) * 2


    df['AQI'] = df['PM2.5'].apply(calculate_aqi)

    # Reorder columns to match your analysis script
    df = df[['City', 'Date', 'PM2.5', 'PM10', 'NO2', 'AQI']]

    # Save
    output_file = 'india_aqi_data.csv'
    df.to_csv(output_file, index=False)

    print(f"✅ Success! Fetched {len(df)} rows of REAL historical data.")
    print(f"📂 Saved to: {output_file}")
    print(df.head())

except Exception as e:
    print(f"❌ Error: {e}")