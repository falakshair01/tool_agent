import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.tool_manager import ToolManager
from app.intent_recognizer import IntentRecognizer
from app.schemas import QueryRequest, QueryResponse

app = FastAPI(title="Tool-Using Agent", version="1.0.0")

# Initialize components
tool_manager = ToolManager()
intent_recognizer = IntentRecognizer()

@app.on_event("startup")
async def startup_event():
    """Register tools on startup."""
    tool_manager.register_tools()

@app.post("/query/", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Main endpoint to process user queries:
    1. Recognize intent
    2. Execute appropriate tool (if applicable)
    3. Generate natural language response
    """
    user_query = request.query.strip()
    if not user_query:
        return JSONResponse({"detail": "Query cannot be empty"}, status_code=400)

    # Step 1: Recognize intent
    intent = intent_recognizer.recognize(user_query)

    # Step 2: If unknown intent => return helpful message
    if intent["type"] == "unknown":
        return QueryResponse(
            query=user_query,
            intent="unknown",
            confidence=0.0,
            tool_used=None,
            tool_output=None,
            response="I couldn't detect an intent. Try asking about math, the current time, or the weather (e.g., '12 + 5', 'what time is it', 'weather in Tokyo')."
        )

    # Step 3: Execute tool via manager
    tool_name = intent.get("tool")
    if not tool_manager.has_tool(tool_name):
        return QueryResponse(
            query=user_query,
            intent=intent["type"],
            confidence=float(intent.get("confidence", 0.0)),
            tool_used=None,
            tool_output=None,
            response=f"Detected intent '{intent['type']}', but the tool '{tool_name}' is not available."
        )

    try:
        _, tool_result = tool_manager.invoke_tool(tool_name, intent.get("parameters", {}), user_query)
    except Exception as e:
        return QueryResponse(
            query=user_query,
            intent=intent["type"],
            confidence=float(intent.get("confidence", 0.0)),
            tool_used=tool_name,
            tool_output={"error": str(e)},
            response=f"Tool execution failed: {str(e)}"
        )

    # Step 4: Build natural-language response
    response_text = _generate_response(intent, tool_result, user_query)

    return QueryResponse(
        query=user_query,
        intent=intent["type"],
        confidence=float(intent.get("confidence", 0.0)),
        tool_used=tool_name,
        tool_output=tool_result,
        response=response_text
    )

@app.get("/")
async def root():
    return {"status": "running", "message": "Tool-Using Agent API is active", "available_tools": tool_manager.list_tools()}

def _generate_response(intent: dict, result: dict, original_query: str) -> str:
    """Generate a natural language response from intent+tool result."""
    intent_type = intent.get("type")
    if intent_type == "calculator":
        if result.get("success"):
            # If calculator provided a 'natural' friendly string, use it; else build one.
            natural = result.get("natural") or f"The result of {result.get('expression') or original_query} is {result.get('result')}."
            return natural
        return f"I couldn't calculate that: {result.get('error', 'invalid expression')}."

    if intent_type == "time":
        if result.get("success"):
            return f"The current time is {result.get('time')} (local)."
        return f"Time query failed: {result.get('error', 'unknown error')}."

    if intent_type == "weather":
        if result.get("success"):
            loc = result.get("location", "your area")
            cond = result.get("condition", "unknown")
            temp = result.get("temperature")
            unit = result.get("unit", "Celsius")
            return f"The weather in {loc} is {cond} with a temperature of {temp}°{unit[0]}."
        return f"Weather query failed: {result.get('error', 'unknown error')}."

    # Fallback
    return "I'm not sure how to help with that. Try asking about math, time, or weather."

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
