from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import math

app = FastAPI(title="Backend API")

@app.get("/weather")
async def get_weather(city: str = Query(...)):
    # Mock weather data
    return {"city": city, "temperature": 22, "condition": "sunny"}

@app.get("/calculate")
async def calculate(expr: str = Query(...)):
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed.update({"abs": abs})
        result = eval(expr, {"__builtins__": {}}, allowed)
        return {"expression": expr, "result": result}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

# ✅ Include Uvicorn here
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)