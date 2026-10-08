#!/usr/bin/env python3
"""Unit tests for weather.py with mocked API calls."""

import unittest
from unittest.mock import patch, MagicMock
import requests
import os
import tempfile
from weather import fetch_weather, weather_code_to_description, print_weather_summary, create_forecast_chart


class TestWeatherCodeToDescription(unittest.TestCase):
    """Test weather code conversion function."""
    
    def test_clear_sky(self):
        self.assertEqual(weather_code_to_description(0), "Clear sky")
    
    def test_partly_cloudy(self):
        self.assertEqual(weather_code_to_description(2), "Partly cloudy")
    
    def test_rain(self):
        self.assertEqual(weather_code_to_description(63), "Moderate rain")
    
    def test_unknown_code(self):
        self.assertEqual(weather_code_to_description(999), "Unknown (999)")


class TestFetchWeather(unittest.TestCase):
    """Test weather data fetching with mocked API."""
    
    @patch('weather.requests.get')
    def test_fetch_weather_success(self, mock_get):
        """Test successful API call."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "current": {
                "time": "2024-01-15T12:00",
                "temperature_2m": 10.5,
                "relative_humidity_2m": 75,
                "weather_code": 2
            },
            "daily": {
                "time": ["2024-01-15", "2024-01-16", "2024-01-17"],
                "temperature_2m_max": [12.0, 11.5, 10.0],
                "temperature_2m_min": [8.0, 7.5, 6.0],
                "weather_code": [2, 3, 1]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call function
        result = fetch_weather()
        
        # Verify
        self.assertIsNotNone(result)
        self.assertIn("current", result)
        self.assertIn("daily", result)
        mock_get.assert_called_once()
    
    @patch('weather.requests.get')
    def test_fetch_weather_api_error(self, mock_get):
        """Test API error handling."""
        mock_get.side_effect = requests.RequestException("API Error")
        
        with self.assertRaises(requests.RequestException):
            fetch_weather()


class TestPrintWeatherSummary(unittest.TestCase):
    """Test weather summary printing."""
    
    @patch('builtins.print')
    def test_print_weather_summary(self, mock_print):
        """Test that summary prints without errors."""
        data = {
            "current": {
                "time": "2024-01-15T12:00",
                "temperature_2m": 10.5,
                "relative_humidity_2m": 75,
                "weather_code": 2
            },
            "daily": {
                "time": ["2024-01-15"],
                "temperature_2m_max": [12.0],
                "temperature_2m_min": [8.0],
                "weather_code": [2]
            }
        }
        
        print_weather_summary(data)
        
        # Verify print was called
        self.assertTrue(mock_print.called)


class TestCreateForecastChart(unittest.TestCase):
    """Test chart generation."""
    
    @patch('weather.plt')
    def test_create_forecast_chart(self, mock_plt):
        """Test chart creation with mocked matplotlib."""
        data = {
            "daily": {
                "time": ["2024-01-15", "2024-01-16"],
                "temperature_2m_max": [12.0, 11.5],
                "temperature_2m_min": [8.0, 7.5],
                "weather_code": [2, 3]
            }
        }
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            create_forecast_chart(data, tmp_path)
            
            # Verify matplotlib functions were called
            self.assertTrue(mock_plt.figure.called)
            self.assertTrue(mock_plt.savefig.called)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
