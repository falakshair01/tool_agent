import random
from typing import Dict, Any

class WeatherQuery:
    """Simulates weather data for a requested location."""

    def __init__(self):
        self.conditions = [
            "sunny", "cloudy", "rainy", "partly cloudy", "stormy",
            "snowy", "foggy", "windy", "clear"
        ]
        self.temp_ranges = {
            "sunny": (22, 35),
            "cloudy": (12, 25),
            "rainy": (8, 20),
            "partly cloudy": (14, 28),
            "stormy": (6, 18),
            "snowy": (-8, 5),
            "foggy": (6, 16),
            "windy": (8, 24),
            "clear": (15, 30)
        }

    def execute(self, user_query: str, params: Dict[str, Any]) -> Dict[str, Any]:
        loc = params.get("location") or "your area"
        loc = loc.strip()
        condition = random.choice(self.conditions)
        tmin, tmax = self.temp_ranges.get(condition, (10, 25))
        temperature = random.randint(tmin, tmax)
        humidity = random.randint(35, 95)
        wind_kmh = random.randint(0, 50)
        return {
            "success": True,
            "location": loc,
            "condition": condition,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed_kmh": wind_kmh,
            "unit": "Celsius",
            "note": "Simulated weather for demo"
        }
