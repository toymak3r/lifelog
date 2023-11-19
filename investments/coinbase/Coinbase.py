import requests
from coinbase.wallet.client import Client
import json
import locale
locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')


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


class Coinbase:

    _client = ''   # Coinbase Client Handler
    _user = ''     # User info

    def __init__(self, api_key, api_secret) -> None:
        self._COINBASE_API_KEY = api_key
        self._COINBASE_API_SECRET = api_secret
        self._client = Client(self._COINBASE_API_KEY,
                              self._COINBASE_API_SECRET)

    def get_user_info(self):
        self._user = self._client.get_current_user()

    def test(self):
        print(f'Name: {self._user["name"]}')
        print(f'ID: {self._user["id"]}')

        accounts = self._client.get_accounts()
        for account in accounts["data"]:
            if float(account["balance"]["amount"]) != 0.0:
                currency = account["currency"]
                if currency == 'ETH2':
                    currency = 'ethereum'
                price = convert_cryptocurrency(
                    currency, float(account["balance"]["amount"]), 'gbp')
                if price != None:
                    print(
                        f'{account["currency"]} : {account["balance"]["amount"]} ({locale.currency(price)})')
