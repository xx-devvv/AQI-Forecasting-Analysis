import requests
import pandas as pd
import numpy as np

# --- STEP 1: FETCH DATA FROM API ---
print("📡 Connecting to OpenAQ API (Real Data)...")

base_url = "https://api.openaq.org/v2/measurements"
params = {
    "city": "Delhi",
    "parameter": ["pm25", "pm10", "no2"],
    "date_from": "2024-01-01",  # Let's get the last ~1 year of data
    "limit": 10000,  # Max per page (we'll use this sample for the demo)
    "format": "json"
}

try:
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'results' not in data or len(data['results']) == 0:
        raise ValueError("API returned no data. Try changing the date_from or city.")

    print(f"✅ Fetched {len(data['results'])} raw data points.")

    # --- STEP 2: PROCESS & CLEAN ---
    # Convert nested JSON to a flat table
    df_raw = pd.json_normalize(data['results'])

    # We only need the date, parameter name, and the value
    df_clean = df_raw[['date.utc', 'parameter', 'value']].copy()
    df_clean['date'] = pd.to_datetime(df_clean['date.utc'])

    # PIVOT THE TABLE: Convert rows (pm25, pm10) into columns
    # We group by Day to get daily averages (smoothing out hourly noise)
    df_pivot = df_clean.pivot_table(index=df_clean['date'].dt.date,
                                    columns='parameter',
                                    values='value',
                                    aggfunc='mean')

    # Rename columns to match what analyze_forecast.py expects
    # OpenAQ returns 'pm25', our script needs 'PM2.5'
    column_map = {'pm25': 'PM2.5', 'pm10': 'PM10', 'no2': 'NO2'}
    df_pivot = df_pivot.rename(columns=column_map)

    # Handle missing columns (e.g., if API didn't return NO2)
    for col in ['PM2.5', 'PM10', 'NO2']:
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan

    # Fill missing values (Forward fill -> assume value stays same until next reading)
    df_pivot = df_pivot.ffill().bfill()


    # --- STEP 3: CALCULATE AQI (Simplified Indian Standard) ---
    # Real AQI calculation is complex; this is a simplified proxy for the project
    def calculate_aqi(row):
        # Approximate breakpoints based on CPCB India
        try:
            pm25_val = row['PM2.5']
            pm10_val = row['PM10']

            # PM2.5 dominates AQI usually. Simple linear proxy:
            if pm25_val <= 30:
                return pm25_val * 1.6
            elif pm25_val <= 60:
                return 50 + (pm25_val - 30) * 1.6
            elif pm25_val <= 90:
                return 100 + (pm25_val - 60) * 3.3
            elif pm25_val <= 120:
                return 200 + (pm25_val - 90) * 3.3
            else:
                return 300 + (pm25_val - 120) * 2  # Hazardous
        except:
            return 150  # Default fallback


    df_pivot['AQI'] = df_pivot.apply(calculate_aqi, axis=1)

    # Final Formatting
    df_final = df_pivot.reset_index()
    df_final.rename(columns={'date': 'Date'}, inplace=True)
    df_final['City'] = 'Delhi'

    # Reorder columns
    df_final = df_final[['City', 'Date', 'PM2.5', 'PM10', 'NO2', 'AQI']]

    # --- STEP 4: SAVE ---
    output_file = 'india_aqi_data.csv'
    df_final.to_csv(output_file, index=False)
    print(f"🎉 Success! Real API data processed and saved to '{output_file}'")
    print(df_final.head())

except Exception as e:
    print(f"❌ Error: {e}")
    print("Tip: Check your internet connection or API rate limits.")