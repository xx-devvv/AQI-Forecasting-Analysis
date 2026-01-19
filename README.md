# 🌍 Air Quality Index (AQI) Analysis & Forecasting

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Statsmodels](https://img.shields.io/badge/Statsmodels-Forecasting-orange)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-green)

A comprehensive Data Science project analyzing historical air quality data from **Delhi** (2023-2025) to identify seasonal pollution trends, forecast future AQI levels, and recommend data-driven policy interventions.

---

## 📖 Project Overview
Air pollution in major Indian cities follows a predictable but severe seasonal cycle. This project aims to:
1.  **Analyze** historical AQI data to visualize the "Winter Smog" phenomenon.
2.  **Forecast** future pollution levels using Time Series models (ARIMA vs. Holt-Winters).
3.  **Visualize** live trends using an interactive Streamlit dashboard.
4.  **Suggest** actionable policy interventions based on predictive data.

### Key Insights:
* **Severe Winter Spikes:** AQI consistently crosses 350+ during November-January due to temperature inversion and stubble burning.
* **Monsoon Relief:** Air quality improves significantly (AQI < 60) during July-September.
* **Model Selection:** While **Holt-Winters** visually captured the seasonal peaks better, **ARIMA** proved to be statistically more stable for general trend forecasting.

---

## 🛠️ Tech Stack
* **Data Engineering:** Python, Pandas, Open-Meteo API (Real-time data fetching)
* **Visualization:** Matplotlib (Static Reports), Plotly & Streamlit (Interactive Dashboard)
* **Machine Learning & Forecasting:**
    * **ARIMA:** AutoRegressive Integrated Moving Average (Trend-focused).
    * **Holt-Winters:** Exponential Smoothing (Seasonality-focused).

---

## 📂 Project Structure

```text
AQI_Analysis/
│
├── fetch_data_v2.py       # Data Pipeline: Fetches real historical data from Open-Meteo API
├── analyze_forecast.py    # Analysis: Performs EDA and trains the ARIMA model
├── compare_models.py      # Evaluation: Compares ARIMA vs Holt-Winters (RMSE scores)
├── dashboard.py           # UI: Interactive Web Dashboard (Streamlit + Plotly)
├── requirements.txt       # Project Dependencies
├── README.md              # Documentation & Policy Report
│
└── (Generated Output)
    ├── india_aqi_data.csv # The dataset
    ├── aqi_trend.png      # Static Trend Graph
    ├── aqi_forecast.png   # Static Forecast Graph
    └── model_comparison.png # Model Comparison Graph
```

---

## 🚀 Installation & Usage

### 1. Clone & Install Dependencies
```bash
git clone [https://github.com/yourusername/aqi-forecasting-project.git](https://github.com/yourusername/aqi-forecasting-project.git)
cd aqi-forecasting-project
pip install -r requirements.txt
```

### 2. Fetch Real-Time Data
Pull the latest historical data for Delhi:
```bash
python fetch_data_v2.py
```

### 3. Run Analysis Reports
Generate static graphs for reports (Trend & Forecast):
```bash
python analyze_forecast.py
```

### 4. Compare Models
Run the competition between ARIMA and Seasonal Holt-Winters:
```bash
python compare_models.py
```

### 5. Launch Interactive Dashboard
Open the web interface to explore the data:
```bash
streamlit run dashboard.py
```

---

## 📊 Model Evaluation Results

| Model | RMSE Score | Strength |
| :--- | :--- | :--- |
| **ARIMA** | **Lower (Better)** | Excellent at following the general yearly trend without overreacting to noise. |
| **Holt-Winters** | Higher | Better at capturing the extreme volatility of winter smog spikes. |

> **Technical Note:** We prioritized **Holt-Winters (Exponential Smoothing)** over Facebook Prophet for the seasonal component to ensure lightweight deployment and avoid C++ dependency issues on Windows environments.

---

## 📢 Policy & Public Health Recommendations
Based on our time-series analysis identifying severe winter spikes (AQI 350+), we recommend:

### 🏛️ Government Policy
1.  **Automated GRAP Enforcement:** Trigger the *Graded Response Action Plan* (GRAP) automatically when the model forecasts AQI > 300 for 3 consecutive days.
2.  **Smart Odd-Even Rule:** Instead of random dates, apply the Odd-Even vehicle rule *only* during the "Red Zone" weeks identified by the Holt-Winters model.
3.  **Stubble Burning Subsidies:** Focus financial aid for "Happy Seeder" machines specifically in October-November to prevent the initial winter spike.

### 😷 Public Health
1.  **School Timings:** Shift school start times to 10:00 AM or switch to online classes when the ARIMA model predicts morning smog.
2.  **Early Warning System:** Issue health advisories 48 hours in advance based on model predictions, allowing hospitals to prepare for respiratory cases.

---

## 👨‍💻 Author
**Dev Pandey**
* **Role:** Software Engineer

---

## 📝 License
This project is open-source and available for educational purposes.
