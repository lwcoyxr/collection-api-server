# 🛰️ OpenSense Exporter

A simple Prometheus exporter that collects sensor data from an [openSenseMap](https://opensensemap.org/) senseBox and exposes it at `/metrics` for scraping by Prometheus — ready for visualization in Grafana.


- Pulls **temperature** and **radiation level** data from a public or authenticated senseBox.
- Exposes real-time metrics on `/metrics` in Prometheus format.


## Getting Started

1. Clone the repo.
2. Fill in your senseBox ID and sensor IDs & add your sensors in `opensense_exporter.py`
3. Run with Docker Compose:

   ```bash
   docker-compose up --build
