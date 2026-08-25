from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re

app = FastAPI(title="MCP Client Service")

MCP_SERVER_URL = "http://localhost:8001/rpc"

class UserRequest(BaseModel):
    text: str

def parse_intent(text: str):
    lower = text.lower()
    if "weather" in lower:
        match = re.search(r'in\s+([a-zA-Z\s]+)', text)
        city = match.group(1).strip() if match else text.split()[-1]
        return "get_weather", {"city": city}
    elif "calc" in lower or "calculate" in lower:
        match = re.search(r'(?:calc|calculate)\s+(.+)', text, re.IGNORECASE)
        expr = match.group(1).strip() if match else text
        return "calculate", {"expression": expr}
    else:
        return None, None

@app.post("/chat")
async def chat(request: UserRequest):
    tool, args = parse_intent(request.text)
    if not tool:
        return {"response": "I don't understand. Try 'weather in Paris' or 'calc 3*7'."}

    # Build JSON-RPC request for the MCP Server
    payload = {
        "jsonrpc": "2.0",
        "method": "call_tool",
        "params": {"name": tool, "arguments": args},
        "id": 1
    }

    try:
        resp = requests.post(MCP_SERVER_URL, json=payload, timeout=5)
        data = resp.json()
        error = data.get("error") if isinstance(data, dict) else None
        if error :
            return {"response": f"MCP Server Error: {data['error']['message']}"}
        result= data.get("result") if isinstance(data, dict) else None
        content = data.get("result", {}).get("content", [])
        if content:
            return {"response": content[0].get("text", "No response text")}
        return {"response": "No content returned from tool."}
    
    except Exception as e:
        return {"response": f"Client Error: {str(e)}"}

# ✅ Include Uvicorn here
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)