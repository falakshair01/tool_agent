import re
from typing import Dict, Any

class Calculator:
    """Safe calculator tool. Supports numeric expressions and simple natural language."""

    def execute(self, user_query: str, params: Dict[str, Any]) -> Dict[str, Any]:
        # Prefer explicit parsed expression passed by intent recognizer
        expr = params.get("expression") or user_query

        # Clean expression: only allow digits, operators, parentheses, decimal point and spaces
        cleaned = re.sub(r'[^0-9\.\+\-\*\/\(\)\s]', '', expr)
        cleaned = cleaned.strip()
        # If still no operator, fail
        if not re.search(r'[\+\-\*\/]', cleaned):
            return {"success": False, "error": "No arithmetic operation found", "expression": expr}

        # Evaluate safely: allow only allowed characters
        try:
            # Very small safety: confirm only allowed chars remain
            if not re.fullmatch(r'[\d\.\+\-\*\/\(\)\s]+', cleaned):
                return {"success": False, "error": "Unsafe characters in expression", "expression": expr}
            # Use eval in restricted globals
            result = eval(cleaned, {"__builtins__": {}}, {})
            # Normalize result
            if isinstance(result, float):
                result_rounded = round(result, 6)
            else:
                result_rounded = result
            natural = f"{cleaned} = {result_rounded}"
            return {"success": True, "expression": expr, "parsed_expression": cleaned, "result": result_rounded, "natural": natural}
        except ZeroDivisionError:
            return {"success": False, "error": "Division by zero", "expression": expr}
        except Exception as e:
            return {"success": False, "error": f"Evaluation error: {str(e)}", "expression": expr}
