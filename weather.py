#!/usr/bin/env python3
"""Fetch weather and 7-day forecast for London from Open-Meteo API."""

import requests
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, List


def fetch_weather(lat: float = 51.5074, lon: float = -0.1278) -> Dict:
    """Fetch weather data from Open-Meteo API.
    
    Args:
        lat: Latitude (default: London)
        lon: Longitude (default: London)
    
    Returns:
        Dictionary containing weather data
    """
    url = f"https://api.open-meteo.com/v1/forecast"
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


def print_weather_summary(data: Dict) -> None:
    """Print a clean summary of current weather to terminal."""
    current = data["current"]
    daily = data["daily"]
    
    print("\n" + "=" * 50)
    print("LONDON WEATHER")
    print("=" * 50)
    print(f"\nCurrent Weather (as of {current['time']})")
    print("-" * 50)
    print(f"Temperature: {current['temperature_2m']}°C")
    print(f"Humidity: {current['relative_humidity_2m']}%")
    print(f"Conditions: {weather_code_to_description(current['weather_code'])}")
    
    print(f"\n7-Day Forecast")
    print("-" * 50)
    for i in range(len(daily['time'])):
        date = datetime.strptime(daily['time'][i], "%Y-%m-%d").strftime("%a, %b %d")
        temp_max = daily['temperature_2m_max'][i]
        temp_min = daily['temperature_2m_min'][i]
        conditions = weather_code_to_description(daily['weather_code'][i])
        print(f"{date}: {temp_max}°C / {temp_min}°C - {conditions}")
    
    print("\n" + "=" * 50 + "\n")


def create_forecast_chart(data: Dict, output_file: str = "forecast.png") -> None:
    """Create a simple chart of the 7-day temperature forecast.
    
    Args:
        data: Weather data from Open-Meteo API
        output_file: Path to save the PNG chart
    """
    daily = data["daily"]
    
    # Parse dates
    dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%a %d") for d in daily['time']]
    temp_max = daily['temperature_2m_max']
    temp_min = daily['temperature_2m_min']
    
    # Create chart
    plt.figure(figsize=(12, 6))
    plt.plot(dates, temp_max, marker='o', label='Max Temperature', color='red', linewidth=2)
    plt.plot(dates, temp_min, marker='o', label='Min Temperature', color='blue', linewidth=2)
    
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("7-Day Temperature Forecast - London")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Chart saved to {output_file}\n")


def main():
    """Main function to fetch, display, and chart weather data."""
    print("Fetching weather data for London...")
    
    try:
        data = fetch_weather()
        print_weather_summary(data)
        create_forecast_chart(data)
        print("Done!")
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
