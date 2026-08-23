from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="MCP Server")

API_BASE = "http://localhost:8000"

class RPCRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict
    id: int

class RPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: dict = None
    error: dict = None
    id: int

@app.post("/rpc")
async def handle_rpc(request: RPCRequest):
    if request.method != "call_tool":
        return RPCResponse(
            jsonrpc="2.0",
            error={"code": -32601, "message": "Method not found"},
            id=request.id
        )

    tool_name = request.params.get("name")
    args = request.params.get("arguments", {})

    if tool_name == "get_weather":
        city = args.get("city")
        if not city:
            raise HTTPException(400, "Missing city")
        resp = requests.get(f"{API_BASE}/weather", params={"city": city})
        if resp.status_code == 200:
            data = resp.json()
            text = f"Weather in {city}: {data['temperature']}°C, {data['condition']}"
            return RPCResponse(
                jsonrpc="2.0",
                result={"content": [{"type": "text", "text": text}]},
                id=request.id
            )
        else:
            return RPCResponse(
                jsonrpc="2.0",
                error={"code": -32000, "message": "API error"},
                id=request.id
            )

    elif tool_name == "calculate":
        expr = args.get("expression")
        if not expr:
            raise HTTPException(400, "Missing expression")
        resp = requests.get(f"{API_BASE}/calculate", params={"expr": expr})
        if resp.status_code == 200:
            data = resp.json()
            text = f"Result: {data['result']}"
            return RPCResponse(
                jsonrpc="2.0",
                result={"content": [{"type": "text", "text": text}]},
                id=request.id
            )
        else:
            return RPCResponse(
                jsonrpc="2.0",
                error={"code": -32000, "message": "API error"},
                id=request.id
            )

    else:
        return RPCResponse(
            jsonrpc="2.0",
            error={"code": -32601, "message": f"Tool '{tool_name}' not found"},
            id=request.id
        )

# ✅ Include Uvicorn here
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)