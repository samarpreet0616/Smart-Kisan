import requests
from dotenv import load_dotenv
import os

# ---------------- Load API Key ----------------
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")


# ---------------- Current Weather ----------------
def get_current_weather(city):

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": "API request failed"}

        data = response.json()

        if "error" in data:
            return {"error": "City not found"}

        return {
            "temp": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "condition": data["current"]["condition"]["text"],
            "city_name":data["location"]["name"],
            "region":data["location"]["region"]
        }

    except requests.exceptions.RequestException:
        return {"error": "Network error"}


# ---------------- Forecast ----------------
def get_forecast(city):

    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return []

        json_data = response.json()

        if "error" in json_data:
            return []

        forecast_day_list = json_data["forecast"]["forecastday"]

        result_list = []

        for each_day in forecast_day_list:

            one_day = {
                "date": each_day["date"],
                "max_temp": each_day["day"]["maxtemp_c"],
                "min_temp": each_day["day"]["mintemp_c"],
                "condition": each_day["day"]["condition"]["text"],
                "rain_chance": each_day["day"]["daily_chance_of_rain"]
            }

            result_list.append(one_day)

        return result_list

    except requests.exceptions.RequestException:
        return []


# ---------------- Advisory ----------------
def get_advisory(current_data, forecast_data):

    advice_list = []

    today_temp = current_data["temp"]
    today_humidity = current_data["humidity"]

    hot_days = 0
    rainy_days = 0

    for day in forecast_data:

        max_temp = day["max_temp"]
        rain_chance = day["rain_chance"]

        if max_temp > 36:
            hot_days += 1

        if rain_chance > 70:
            rainy_days += 1

    if rainy_days >= 1:
        advice_list.append("Rain expected in next 3 days. Avoid extra irrigation.")

    if rainy_days >= 2:
        advice_list.append("Multiple rainy days ahead. Avoid pesticide spraying.")

    if hot_days == 3:
        advice_list.append("Heat stress likely for next 3 days. Water crops early morning.")

    if today_humidity > 75:
        advice_list.append("Humidity is high. Watch for fungus/pest issues.")

    if today_temp > 38:
        advice_list.append("Very hot today. Reduce midday field work.")

    if advice_list == []:
        advice_list.append("Weather looks stable for next few days.")

    return advice_list


def get_current_weather_by_location(lat,long):



    location = f"{lat},{long}"

    return get_current_weather(location)


def get_forecast_by_location(lat,long):

    location = f"{lat},{long}"

    return get_forecast(location)

