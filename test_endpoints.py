import requests
import pandas as pd
import time

def test_binance_endpoints():
    endpoints = [
        "https://api.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com",
        "https://fapi.binance.com", # Futures API
        "https://dapi.binance.com"  # Delivery API
    ]

    for base_url in endpoints:
        print(f"Testing {base_url}...")
        try:
            url = f"{base_url}/api/v3/ping" if "fapi" not in base_url and "dapi" not in base_url else f"{base_url}/fapi/v1/ping"
            response = requests.get(url, timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"SUCCESS: {base_url} is reachable.")
            else:
                print(f"FAILED: {base_url} returned {response.status_code} - {response.text}")
        except Exception as e:
            print(f"ERROR: {base_url} - {e}")
        print("-" * 20)

if __name__ == "__main__":
    test_binance_endpoints()
