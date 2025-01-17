import requests
from app.config import WEATHER_API_KEY

WEATHER_API_URL = 'http://api.weatherapi.com/v1/current.json'


def get_temperature_in(city: str) -> float:
    response = requests.get(WEATHER_API_URL, params={
        'key': WEATHER_API_KEY,
        'q': city
    })
    temperature = response.json()['current']['temp_c']
    return temperature
