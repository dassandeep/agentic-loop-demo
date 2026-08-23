# agentic-loop-demo
Lightweight Python demo showcasing agentic AI loop: plan, act, reflect with simple tools, illustrating autonomous reasoning and orchestration.

1#
fastapi
uvicorn
requests
pydantic

2#
ExternalAPI/api.py (The Real Backend)
Runs on port 8000. Handles actual weather and calculation logic.
python api.py
Expected output: Uvicorn running on http://0.0.0.0:8000

3#
McpServer/mcp_server.py (The Tool Orchestrator)
Runs on port 8001. Exposes JSON-RPC endpoints and calls the API.
python mcp_server.py
Expected output: Uvicorn running on http://0.0.0.0:8001

4#
Mcpclientservice/mcp_client_service.py (The Gateway / Intent Classifier)
Runs on port 8002. Receives the user's raw text, decides which tool to use, and forwards JSON-RPC to the MCP Server.
python mcp_client_service.py
Expected output: Uvicorn running on http://0.0.0.0:8002

5#
Client/bot.py (The Simple CLI User Interface)
This is the only file without Uvicorn. It just sends HTTP requests to the MCP Client Service.
python bot.py

🤖 AI Bot (Connected to MCP Client Service on port 8002)
Type 'weather in <city>' or 'calc <expression>' or 'exit' to quit.

You: weather in Tokyo
Bot: Weather in Tokyo: 22°C, sunny

You: calc 12 * 8 - 4
Bot: Result: 92

You: hello
Bot: I don't understand. Try 'weather in Paris' or 'calc 3*7'.
------------------------------------------------------------------------
The Agentic Flow (Visual)
[User] 
   ↓ (HTTP)
[Bot.py] 
   ↓ (POST /chat)
[MCP Client Service]  (Parses Intent)
   ↓ (JSON-RPC HTTP)
[MCP Server]  (Routes to Tool)
   ↓ (HTTP GET)
[Backend API]  (Computes result)
   ↑ 
[Response travels back the same way]
