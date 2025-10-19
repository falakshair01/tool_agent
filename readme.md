# Tool-Using Agent (FastAPI)

A clean, minimal Tool-Using Agent implemented in Python using FastAPI.
It demonstrates:
- Tool registration and management
- Rule-based intent recognition
- Calculator, Time, and Weather tools
- Natural language responses

## Project Structure
```
tool_agent/
└── app/
    ├── main.py
    ├── requirements.txt
    ├── init.py
    ├── schemas.py
    ├── intent_recognizer.py
    ├── tool_manager.py
    └── tools/
        ├── init.py
        ├── calculator.py
        ├── time_query.py
        └── weather_query.py
```

## Setup
```bash
python -m venv venv
source venv/bin/activate    
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python uvicorn app.main:app
```
Open: http://127.0.0.1:8000/docs

### Examples

POST /query/ JSON body examples:

Calculator:
```json
{ "query": "What is 25 + 7?" }
```

Time:
```json
{ "query": "What time is it now?" }
```

Weather:
```json
{ "query": "What's the weather in Paris?" }
```

### Notes

- Calculator uses a restricted eval strategy; it allows only numeric and operator characters.
- Weather is simulated for demonstration purposes.
