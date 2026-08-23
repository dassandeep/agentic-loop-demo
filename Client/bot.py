import requests

MCP_CLIENT_URL = "http://localhost:8002/chat"

def main():
    print("🤖 AI Bot (Connected to MCP Client Service on port 8002)")
    print("Type 'weather in <city>' or 'calc <expression>' or 'exit' to quit.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        try:
            response = requests.post(MCP_CLIENT_URL, json={"text": user_input}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"Bot: {data.get('response', 'No response')}")
            else:
                print(f"Bot: HTTP Error {response.status_code}")
        except Exception as e:
            print(f"Bot: Connection Error - {e}")

if __name__ == "__main__":
    main()