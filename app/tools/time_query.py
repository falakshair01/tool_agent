from datetime import datetime
from typing import Dict, Any

class TimeQuery:
    """Returns current local time and related fields."""

    def execute(self, user_query: str, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            now = datetime.now()
            return {
                "success": True,
                "time": now.strftime("%H:%M:%S"),
                "time_12h": now.strftime("%I:%M:%S %p"),
                "date": now.strftime("%Y-%m-%d"),
                "full_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
                "day_of_week": now.strftime("%A")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
