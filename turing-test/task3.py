from fastapi import FastAPI, HTTPException, Body, status
from pydantic import BaseModel
from typing import Dict, Any

# ==========================================
# TASK C: Minimal MCP (Model Context Protocol)
# ==========================================

# Create FastAPI app instance
app = FastAPI()

TOOLS = [
    {
        "name": "sum",
        "description": "Add two numbers",
        "parameters": ["a", "b"]
    }
]
# TODO: 1. Implement GET /tools
# Requirements:
# - Return a JSON object listing available tools.
# - Currently, only support one tool: "sum".
# - "sum" takes parameters "a" and "b".



@app.get("/tools")
async def list_tools():
    return {
        "tools": TOOLS
    }


# TODO: 2. Implement POST /call_tool
# Requirements:
# - Accept JSON: {"tool": "name", "args": { ... }}
# - If tool is "sum", return {"result": a + b}
# - Validate that 'a' and 'b' are numbers.
# - Handle unknown tools or bad arguments with HTTP 400.
@app.post("/call_tool")
async def call_tool(payload: Dict[str, Any] = Body(...)):
    
    tool_name = payload.get("tool")
    args = payload.get("args")

    if tool_name != "sum":
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid arguments"
        )

    if 'a' not in args or 'b' not in args:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "missing arguments"
        )
    
    

    a = args.get("a")
    b = args.get("b")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid arguments"
        )


    result = a + b
    
    
    return { "result": result}