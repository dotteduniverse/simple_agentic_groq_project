import requests
from typing import Dict, Any
from tools.base import BaseTool

class WeatherTool(BaseTool):
    @property
    def name(self) -> str:
        return "weather_tool"

    @property
    def description(self) -> str:
        return "Get current weather conditions for a given location (city, state, country)."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name (e.g., London, New York, Paris). Can include country code.",
                }
            },
            "required": ["location"],
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        location = arguments["location"].strip()
        if not location:
            return "Please provide a location."

        # Use wttr.in - returns JSON with current conditions
        url = f"https://wttr.in/{location}?format=j1"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return f"Weather API error: {str(e)}"

        # Extract useful info
        try:
            current = data["current_condition"][0]
            temp_c = current["temp_C"]
            temp_f = current["temp_F"]
            humidity = current["humidity"]
            wind_speed = current["windspeedKmph"]
            weather_desc = current["weatherDesc"][0]["value"]
            feels_like_c = current["FeelsLikeC"]
            location_name = data["nearest_area"][0]["areaName"][0]["value"]
            country = data["nearest_area"][0]["country"][0]["value"]

            return (
                f"🌤️ Weather in {location_name}, {country}:\n"
                f"  • Conditions: {weather_desc}\n"
                f"  • Temperature: {temp_c}°C / {temp_f}°F (feels like {feels_like_c}°C)\n"
                f"  • Humidity: {humidity}%\n"
                f"  • Wind: {wind_speed} km/h"
            )
        except (KeyError, IndexError) as e:
            return f"Could not parse weather data for '{location}'. Please check the spelling or try a different location."