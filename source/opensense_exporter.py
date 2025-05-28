from prometheus_client import start_http_server, Gauge
import httpx
import time

SENSEBOX_ID = "your_sensebox_id"
EXPORT_PORT = 8000

# Define gauges
temperature_gauge = Gauge(
    "opensense_temperature_celsius", 
    "Temperature in Celsius (Sensor: DHT22)"
)

radiation_gauge = Gauge(
    "opensense_gamma_radiation_microsieverts_per_hour", 
    "Gamma radiation in µSv/h (Sensor: SBM-20)"
)

def fetch_data():
    url = f"https://api.opensensemap.org/boxes/{SENSEBOX_ID}"
    try:
        r = httpx.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        for sensor in data.get("sensors", []):
            title = sensor.get("title", "").lower()
            value = float(sensor.get("lastMeasurement", {}).get("value", 0))
            
            if "temperature" in title:
                temperature_gauge.set(value)

            elif "radiation" in title or "µsv" in title:
                radiation_gauge.set(value)

    except Exception as e:
        print(f"Error fetching or parsing data: {e}")

if __name__ == "__main__":
    print(f"Starting Prometheus exporter on port {EXPORT_PORT}")
    start_http_server(EXPORT_PORT)
    
    while True:
        fetch_data()
        time.sleep(30)  # Poll every 30s
