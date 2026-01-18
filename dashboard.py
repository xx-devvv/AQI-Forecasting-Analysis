import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup
st.set_page_config(page_title="AQI Forecasting Dashboard", layout="wide")
st.title("🌍 AI Air Quality Forecasting Dashboard")


# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('india_aqi_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df


try:
    df = load_data()

    # 3. Sidebar Controls
    st.sidebar.header("Filter Options")
    selected_city = st.sidebar.selectbox("Select City", df['City'].unique())

    # 4. Interactive Plot (Plotly)
    st.subheader(f"📊 Live AQI Trends for {selected_city}")

    city_data = df[df['City'] == selected_city]

    # Create interactive line chart
    fig = px.line(city_data, x='Date', y='AQI', title=f'{selected_city} AQI History')

    # Add a red line for "Danger Zone"
    fig.add_hline(y=200, line_dash="dash", line_color="red", annotation_text="Poor Quality Threshold")

    st.plotly_chart(fig, use_container_width=True)

    # 5. Show Metrics
    avg_aqi = city_data['AQI'].mean()
    max_aqi = city_data['AQI'].max()

    col1, col2 = st.columns(2)
    col1.metric("Average AQI", f"{avg_aqi:.0f}")
    col2.metric("Max Recorded AQI", f"{max_aqi:.0f}", delta_color="inverse")

except FileNotFoundError:
    st.error("Error: 'india_aqi_data.csv' not found. Please run fetch_data_v2.py first.")