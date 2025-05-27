import requests


class OpenMeteo(object):
    def __init__(self, language="en"):
        self.language = language

    def get_cities_results_by_name(self, city: str):
        response = requests.get(
            f"https://geocoding-api.open-meteo.com/v1//search?name={city}&count=1&language={self.language}&format=json"
        )
        return response.json()

    def get_current_forecast_by_coordinates(self, city: str, latitude: float, longitude: float):
        forecast = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        ).json()
        if "error" in forecast:
            return None

        data = {
            "city": city,
            "temperature": forecast["current_weather"]["temperature"],
            "windspeed": forecast["current_weather"]["windspeed"],
            "time": forecast["current_weather"]["time"]
        }
        return data

    def get_hourly_forecast_by_coordinates(self, latitude: float, longitude: float):
        hourly_data = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation,weathercode&timezone=Europe/Moscow"
        ).json()
        if "error" in hourly_data:
            return None

        return hourly_data.get("hourly", {})

    def get_hisotrical_forecast_by_coordinates(self, latitude: float, longitude: float):
        historical_data = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Moscow"
        ).json()
        if "error" in historical_data:
            return None

        return historical_data.get("daily", {})