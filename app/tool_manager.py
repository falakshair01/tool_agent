from typing import Callable, Dict, Any, Tuple, List

# Import tool classes (these are defined in app/tools)
from app.tools.calculator import Calculator
from app.tools.time_query import TimeQuery
from app.tools.weather_query import WeatherQuery

class ToolManager:
    """
    Central registry and invoker for tools.
    Register tools in register_tools(), then use invoke_tool(name, params, user_query).
    """

    def __init__(self):
        self.tools: Dict[str, Callable[..., Any]] = {}

    def register_tools(self):
        """Instantiate and register all tool classes."""
        self.tools["calculator"] = Calculator()
        self.tools["time"] = TimeQuery()
        self.tools["weather"] = WeatherQuery()

    def has_tool(self, name: str) -> bool:
        return name in self.tools

    def invoke_tool(self, name: str, params: Dict[str, Any], user_query: str) -> Tuple[str, Dict[str, Any]]:
        """
        Call a tool by name with parameters.
        Returns (tool_name, result_dict).
        """
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered.")
        tool = self.tools[name]
        # Each tool exposes execute(user_query, params)
        result = tool.execute(user_query, params or {})
        return name, result

    def list_tools(self) -> List[str]:
        return list(self.tools.keys())
