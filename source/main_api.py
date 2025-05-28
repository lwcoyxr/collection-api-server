from fastapi import FastAPI
import httpx

app = FastAPI()

SENSEBOX_ID = "your_sensebox_id_here"

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/latest")
async def get_latest_measurements():
    url = f"https://api.opensensemap.org/boxes/{SENSEBOX_ID}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
    data = r.json()
    return {
        "name": data["name"],
        "sensors": [
            {
                "title": sensor["title"],
                "lastMeasurement": sensor.get("lastMeasurement", {})
            } for sensor in data["sensors"]
        ]
    }