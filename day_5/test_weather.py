import pytest
from unittest.mock import patch
from weather import WeatherAlertService

@pytest.fixture
def service():
    return WeatherAlertService()

@patch('weather.get_temperature')
def test_weather_alert_returns_high(mock_get, service):
    mock_get.return_value = 55
    assert service.get_alert() == "HIGH"

@patch('weather.get_temperature')
def test_weather_alert_returns_normal(mock_get, service):
    mock_get.return_value = 30
    assert service.get_alert() == "NORMAL"

@patch('weather.get_temperature')
def test_weather_alert_returns_low(mock_get, service):
    mock_get.return_value = 5
    assert service.get_alert() == "LOW"