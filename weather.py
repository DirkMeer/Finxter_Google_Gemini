import os
from json import dumps

import requests
from dotenv import load_dotenv

load_dotenv()


def get_current_weather(location: str) -> str:
    """Get the current weather for a location using the WeatherAPI.
    
    Args:
        location (str): The location to get the current weather for, e.g. "London".

    Returns:
        str: A JSON string containing the current weather data in detail.
    """
    if not location:
        return (
            "Please provide a location and call the get_current_weather_function again."
        )
    API_params = {
        "key": os.environ["WEATHER_API_KEY"],
        "q": location,
        "aqi": "no",
        "alerts": "no",
    }
    response = requests.get(
        "http://api.weatherapi.com/v1/current.json", params=API_params
    )
    str_response: str = dumps(response.json())
    return str_response


def get_weather_forecast(location: str, days: int = 7) -> str:
    """Get the weather forecast for a location using the WeatherAPI.

    Args:
        location (str): The location to get the weather forecast for.
        days (int, optional): The number of days to get the forecast for. Defaults to 7.

    Returns:
        str: A JSON string containing the weather forecast data in detail.
    """
    print(type(days))
    try:
        days = int(days)
        days = 1 if days < 1 else 14 if days > 14 else days
    except (TypeError, ValueError):
        days = 7

    params = {
        "key": os.environ["WEATHER_API_KEY"],
        "q": location,
        "days": days,
        "aqi": "no",
        "alerts": "no",
    }

    print(f"Getting weather forecast for {location} for {days} days.")

    response = requests.get(
        "http://api.weatherapi.com/v1/forecast.json", params=params
    )

    forecast_data: dict = response.json()
    filtered_response = {}
    filtered_response["location"] = forecast_data["location"]
    filtered_response["current"] = forecast_data["current"]
    filtered_response["forecast"] = [
        [day["date"], day["day"]] for day in forecast_data["forecast"]["forecastday"]
    ]
    return dumps(filtered_response)


if __name__ == "__main__":
    # print(get_current_weather("Seoul"))
    # print(get_current_weather("Amsterdam"))
    print(get_weather_forecast("Seoul", days=3))