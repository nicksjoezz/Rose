import requests

def test_binance_testnet():
    testnet_url = "https://testnet.binancefuture.com/fapi/v1/ping"
    print(f"Testing {testnet_url}...")
    try:
        response = requests.get(testnet_url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS: Binance Futures Testnet is reachable.")
        else:
            print(f"FAILED: Testnet returned {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_binance_testnet()
