# London Weather Forecast

A Python application that fetches the current weather and 7-day forecast for London from the Open-Meteo API. Available as both a CLI script and a web app.

## Features

- Fetches current weather conditions (temperature, humidity, weather description)
- Displays a clean 7-day forecast summary
- Generates a PNG chart showing the temperature forecast
- Interactive web app with Streamlit
- No API key required (uses free Open-Meteo API)

## Requirements

- Python 3.7+
- requests
- matplotlib
- streamlit (for web app)

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### CLI Version

Run the script:

```bash
python weather.py
```

This will:
1. Fetch weather data for London from the Open-Meteo API
2. Print a formatted summary to the terminal
3. Save a temperature forecast chart as `forecast.png`

### Web App (Streamlit)

Run the Streamlit app locally:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Example Output

```
==================================================
LONDON WEATHER
==================================================

Current Weather (as of 2024-01-15T12:00)
--------------------------------------------------
Temperature: 10.5°C
Humidity: 75%
Conditions: Partly cloudy

7-Day Forecast
--------------------------------------------------
Mon, Jan 15: 12.0°C / 8.0°C - Partly cloudy
Tue, Jan 16: 11.5°C / 7.5°C - Overcast
...

==================================================
```

## Running Tests

Run the unit tests:

```bash
python test_weather.py
```

The tests include mocked API calls, so they can run without network access.

## Deployment

### Streamlit Community Cloud

The app is deployed on Streamlit Community Cloud. To deploy your own version:

1. **Fork this repository** on GitHub
2. **Sign up** at [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub account** to Streamlit
4. **Click "New app"** and select:
   - Repository: Your forked repository
   - Branch: `main` or `feature/weather-forecast`
   - Main file path: `app.py`
5. **Click "Deploy"**

The app will be deployed automatically and you'll get a public URL.

## API

This script uses the [Open-Meteo API](https://open-meteo.com/), a free open-source weather API that requires no API key.

## License

MIT
