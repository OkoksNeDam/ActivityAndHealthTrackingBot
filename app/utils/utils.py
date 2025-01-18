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


def calc_water_intake(weight: float, activity_level: float, city: str):
    temperature = get_temperature_in(city)
    required_water_amount = weight * 30 + 500 * activity_level / 30 + (500 if temperature > 25 else 0)
    required_water_amount /= 1000
    return required_water_amount
