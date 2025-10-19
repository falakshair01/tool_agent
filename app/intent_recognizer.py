import re
from typing import Dict, Any

class IntentRecognizer:
    """
    Rule-based intent recognizer that matches simple math expressions,
    time-related queries and weather-related queries.
    Returns a dict: { type, tool, parameters, confidence }
    """

    def __init__(self):
        self.math_pattern = re.compile(r'(-?\d+(?:\.\d+)?\s*[\+\-\*\/]\s*-?\d+(?:\.\d+)?)')
        # words mapping for written operators
        self.op_words = {
            r'\bplus\b': '+',
            r'\bminus\b': '-',
            r'\btimes\b': '*',
            r'\bmultiplied by\b': '*',
            r'\bdivided by\b': '/',
            r'\bover\b': '/'
        }
        self.time_keywords = ['time', "what time", "current time", "now"]
        self.weather_keywords = ['weather', 'forecast', 'temperature', 'temp', 'rain', 'sunny', 'cloudy']

    def recognize(self, user_query: str) -> Dict[str, Any]:
        q = user_query.strip()
        q_lower = q.lower()

        # 1. Math detection (expressions or textual)
        # Replace textual ops to symbols and search
        normalized = q_lower
        for pat, sym in self.op_words.items():
            normalized = re.sub(pat, sym, normalized)

        # If explicit numeric operator expression found
        m = self.math_pattern.search(normalized)
        if m:
            expr = m.group(1)
            return {
                "type": "calculator",
                "tool": "calculator",
                "parameters": {"expression": expr},
                "confidence": 0.98
            }

        # 2. Math spelled out like "what is 5 plus 3"
        if any(word in q_lower for word in ['plus', 'minus', 'times', 'multiplied', 'divided', 'over']):
            # attempt to convert to expression
            expr_candidate = q_lower
            for pat, sym in self.op_words.items():
                expr_candidate = re.sub(pat, sym, expr_candidate)
            # extract numbers and operators only
            expr_candidate = re.sub(r'[^0-9\.\+\-\*\/\s\(\)]', ' ', expr_candidate)
            # collapse spaces
            expr_candidate = re.sub(r'\s+', ' ', expr_candidate).strip()
            if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', expr_candidate):
                expr = re.search(r'\d+\s*[\+\-\*\/]\s*\d+', expr_candidate).group(0)
                return {"type": "calculator", "tool": "calculator", "parameters": {"expression": expr}, "confidence": 0.9}
            else:
                return {"type": "calculator", "tool": "calculator", "parameters": {"expression": q}, "confidence": 0.6}

        # 3. Time detection
        if any(k in q_lower for k in self.time_keywords):
            return {"type": "time", "tool": "time", "parameters": {}, "confidence": 0.9}

        # 4. Weather detection (try extract location)
        if any(k in q_lower for k in self.weather_keywords):
            location = self._extract_location(q_lower)
            return {"type": "weather", "tool": "weather", "parameters": {"location": location}, "confidence": 0.85}

        # Default: unknown intent
        return {"type": "unknown", "tool": None, "parameters": {}, "confidence": 0.0}

    def _extract_location(self, text: str) -> str:
        # look for "in <Location>" or "for <Location>"
        m = re.search(r'\b(?:in|for)\s+([a-zA-Z\-\s]+)', text)
        if m:
            # trim common trailing words
            loc = m.group(1).strip()
            # stop at next keyword like 'today' or 'now'
            loc = re.split(r'\b(?:today|now|tomorrow|please)\b', loc)[0].strip()
            return loc
        # fallback: last token if alphabetic
        tokens = text.strip().split()
        if tokens and tokens[-1].isalpha():
            return tokens[-1]
        return "your area"
