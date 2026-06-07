from prometheus_client import start_http_server, Gauge
import requests
import time

# Create a metric to track confidence score
CONFIDENCE_GAUGE = Gauge('prediction_confidence_score', 'Latest prediction confidence score from the ML API')

def fetch_latest_confidence():
    url = "http://localhost:32500/api/latest-confidence"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data.get("confidence", 1.0))
    except Exception as e:
        print(f"Error fetching metrics: {e}")
    return 1.0

if __name__ == '__main__':
    # Start up the server to expose the metrics on port 8000
    start_http_server(8000)
    print("Prometheus exporter running on port 8000")
    # Poll every 5 seconds
    while True:
        confidence = fetch_latest_confidence()
        CONFIDENCE_GAUGE.set(confidence)
        time.sleep(5)
