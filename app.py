#!/usr/bin/env python3
"""Streamlit app for displaying London weather forecast."""

import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict


def fetch_weather(lat: float = 51.5074, lon: float = -0.1278) -> Dict:
    """Fetch weather data from Open-Meteo API.
    
    Args:
        lat: Latitude (default: London)
        lon: Longitude (default: London)
    
    Returns:
        Dictionary containing weather data
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "timezone": "Europe/London"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def weather_code_to_description(code: int) -> str:
    """Convert Open-Meteo weather code to human-readable description."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        95: "Thunderstorm",
    }
    return weather_codes.get(code, f"Unknown ({code})")


def create_forecast_chart(data: Dict):
    """Create a simple chart of the 7-day temperature forecast."""
    daily = data["daily"]
    
    # Parse dates
    dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%a %d") for d in daily['time']]
    temp_max = daily['temperature_2m_max']
    temp_min = daily['temperature_2m_min']
    
    # Create chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, temp_max, marker='o', label='Max Temperature', color='red', linewidth=2)
    ax.plot(dates, temp_min, marker='o', label='Min Temperature', color='blue', linewidth=2)
    
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("7-Day Temperature Forecast - London")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="London Weather Forecast",
        page_icon="🌤️",
        layout="wide"
    )
    
    st.title("🌤️ London Weather Forecast")
    st.markdown("Real-time weather and 7-day forecast powered by Open-Meteo API")
    
    # Add refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    # Fetch weather data
    with st.spinner("Fetching weather data..."):
        try:
            data = fetch_weather()
        except requests.RequestException as e:
            st.error(f"Error fetching weather data: {e}")
            return
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return
    
    # Display current weather
    current = data["current"]
    daily = data["daily"]
    
    st.subheader("Current Weather")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Temperature",
            value=f"{current['temperature_2m']}°C"
        )
    
    with col2:
        st.metric(
            label="Humidity",
            value=f"{current['relative_humidity_2m']}%"
        )
    
    with col3:
        st.metric(
            label="Conditions",
            value=weather_code_to_description(current['weather_code'])
        )
    
    st.caption(f"Last updated: {current['time']}")
    
    # Display 7-day forecast
    st.subheader("7-Day Forecast")
    
    # Create forecast table
    forecast_data = []
    for i in range(len(daily['time'])):
        date = datetime.strptime(daily['time'][i], "%Y-%m-%d").strftime("%a, %b %d")
        temp_max = daily['temperature_2m_max'][i]
        temp_min = daily['temperature_2m_min'][i]
        conditions = weather_code_to_description(daily['weather_code'][i])
        forecast_data.append({
            "Date": date,
            "Max Temp (°C)": temp_max,
            "Min Temp (°C)": temp_min,
            "Conditions": conditions
        })
    
    st.dataframe(forecast_data, use_container_width=True)
    
    # Display chart
    st.subheader("Temperature Forecast Chart")
    fig = create_forecast_chart(data)
    st.pyplot(fig)
    
    # Footer
    st.markdown("---")
    st.markdown("Data provided by [Open-Meteo API](https://open-meteo.com/) - Free open-source weather API")


if __name__ == "__main__":
    main()
