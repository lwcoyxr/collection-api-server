import os
import httpx
import time
from prometheus_client import start_http_server, Gauge

SENSEBOX_ID = os.getenv("SENSEBOX_ID", "6836076f69936b0008d4007a")
EXPORT_PORT = 8000

# Prometheus Gauges
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
            measurement = sensor.get("lastMeasurement")

            if not measurement:
                print(f"No measurement for sensor: {title}")
                continue

            value_str = measurement.get("value")
            try:
                value = float(value_str)
            except (ValueError, TypeError):
                print(f"Invalid value for sensor {title}: {value_str}")
                continue

            print(f"{title} = {value}")

            if "temperature" in title:
                temperature_gauge.set(value)

            elif "radiation" in title:
                radiation_gauge.set(value)

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    print(f"📡 Starting Prometheus exporter on port {EXPORT_PORT}")
    start_http_server(EXPORT_PORT)
    
    while True:
        fetch_data()
        time.sleep(30)