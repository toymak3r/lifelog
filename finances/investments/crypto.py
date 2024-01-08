import requests
# Function to get cryptocurrency values

def get_cryptocurrency_value(crypto_symbol, currency='usd'):
    try:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_symbol}&vs_currencies={currency}'
        response = requests.get(url)
        response_data = response.json()
        if crypto_symbol.lower() in response_data:
            return response_data[crypto_symbol.lower()][currency.lower()]
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def convert_cryptocurrency(crypto_symbol, amount, currency='usd'):
    crypto_value = get_cryptocurrency_value(crypto_symbol, currency)
    if crypto_value is not None:
        converted_value = amount * crypto_value
        return converted_value
    else:
        return None
