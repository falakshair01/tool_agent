from pydantic import BaseModel
from typing import Optional, Any, Dict

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    intent: Optional[str]
    confidence: float
    tool_used: Optional[str]
    tool_output: Optional[Dict[str, Any]]
    response: str
