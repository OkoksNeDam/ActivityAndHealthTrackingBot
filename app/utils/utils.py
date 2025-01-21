import pandas as pd
import requests
from aiogram.types import BufferedInputFile
import plotly.express as px

from app.config import WEATHER_API_KEY
from enum import Enum

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
FOOD_INFO_API_URL = "https://world.openfoodfacts.org/cgi/search.pl"


class WorkoutType(Enum):
    STRENGTH_WORKOUT = 'силовая'
    CARDIO_WORKOUT = 'кардио'
    FUNCTIONAL_WORKOUT = 'функциональная'
    DANCE_WORKOUT = 'танцы'
    YOGA_WORKOUT = 'йога'


def get_temperature_in(city: str) -> float:
    """
    Get temperature in selected city using API.
    :param city: city fot which you need to find the temperature.
    :return: temperature in selected city.
    """
    response = requests.get(WEATHER_API_URL, params={
        'key': WEATHER_API_KEY,
        'q': city
    })
    temperature = response.json()['current']['temp_c']
    return temperature


def calc_water_intake(weight: float, activity_level: float, city: str) -> float:
    """
    Calculation of the norm of water consumption using the formula:
    weight * 30 + 500 * activity_level / 30 + 500 * [temperature > 25]
    :param weight: weight of person.
    :param activity_level: activity_level of person.
    :param city: current person's city.
    :return: water norm in ml.
    """
    temperature = get_temperature_in(city)
    required_water_amount = weight * 30 + 500 * activity_level / 30 + (500 if temperature > 25 else 0)
    required_water_amount /= 1000
    return required_water_amount


def calc_calories_intake(weight: float, height: float, age: int) -> float:
    """
    Calculation of calorie intake using the following formula:
    10 * weight + 6.5 * height - 5 * age.
    :param weight:
    :param height:
    :param age:
    :return:
    """
    return 10 * weight + 6.5 * height - 5 * age


def calc_burned_calories_from_workout(workout_type: WorkoutType, workout_duration: int) -> float:
    """
    Calculation of calories burned.

    Calculate calories burned by workout type and duration. For each type of workout,
    the number of calories burned will be different.

    The total number of calories is calculated using the following formula: duration * duration_factor

    :param workout_type: type of workout.
    :param workout_duration: duration of workout in minutes.
    :return: number of burned calories.
    """
    workout_duration_factor = {
        WorkoutType.STRENGTH_WORKOUT: 10,
        WorkoutType.CARDIO_WORKOUT: 15,
        WorkoutType.DANCE_WORKOUT: 8,
        WorkoutType.FUNCTIONAL_WORKOUT: 3,
        WorkoutType.YOGA_WORKOUT: 3
    }

    return workout_duration * workout_duration_factor[workout_type]


def get_calories_of(product_name: str) -> float:
    """
    Find number of product calories using API.
    :param product_name: name of the product for which calories are being searched.
    :return: number of product calories.
    """
    response = requests.get(FOOD_INFO_API_URL, params={
        'action': 'process',
        'search_terms': product_name,
        'json': 'true'
    })
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        # Checking if there are any products found.
        if products:
            first_product = products[0]
            return first_product.get('nutriments', {}).get('energy-kcal_100g', 0)
    print(f"Ошибка: {response.status_code}")


def create_line_chart(x: list, y: list, x_label: str, y_label: str,
                      file_type: str = "png", filename: str = "file.txt") -> BufferedInputFile:
    """
    Creating line chart from x and y data.
    """
    water_consumption_fig = px.line(pd.DataFrame({y_label: y, x_label: x}), x=x_label, y=y_label)

    img_bytes = water_consumption_fig.to_image(format=file_type)
    text_file = BufferedInputFile(img_bytes, filename=filename)

    return text_file
