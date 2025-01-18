import requests
from app.config import WEATHER_API_KEY

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
FOOD_INFO_API_URL = "https://world.openfoodfacts.org/cgi/search.pl"


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


def get_calories_of(product_name: str) -> float:
    response = requests.get(FOOD_INFO_API_URL, params={
        'action': 'process',
        'search_terms': product_name,
        'json': 'true'
    })
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        if products:  # Проверяем, есть ли найденные продукты
            first_product = products[0]
            return first_product.get('nutriments', {}).get('energy-kcal_100g', 0)
    print(f"Ошибка: {response.status_code}")
