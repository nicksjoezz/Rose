import ccxt

def check_rose_availability():
    exchanges = ['gateio', 'kucoin', 'okx', 'bybit', 'mexc']
    for ex_id in exchanges:
        try:
            ex = getattr(ccxt, ex_id)()
            markets = ex.load_markets()
            symbols = [s for s in markets if 'ROSE/USDT' in s]
            if symbols:
                print(f"{ex_id} has {symbols}")
            else:
                print(f"{ex_id} does not have ROSE/USDT")
        except Exception as e:
            print(f"Error checking {ex_id}: {e}")

if __name__ == "__main__":
    check_rose_availability()
