import locale
from ..crypto import convert_cryptocurrency
from coinbase.wallet.client import Client

locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')


class Coinbase:

    _client = ''   # Coinbase Client Handler
    _user = ''     # User info
    _coins = {}

    def __init__(self, api_key, api_secret) -> None:
        self._COINBASE_API_KEY = api_key
        self._COINBASE_API_SECRET = api_secret
        self._client = Client(self._COINBASE_API_KEY,
                              self._COINBASE_API_SECRET)
        self.get_user_info()

    def get_user_info(self):
        self._user = self._client.get_current_user()

    def update_balance(self):
        print(f'Name: {self._user["name"]}')
        print(f'ID: {self._user["id"]}')

        accounts = self._client.get_accounts()
        for account in accounts["data"]:
            if float(account["balance"]["amount"]) != 0.0:
                currency = account["currency"]['code']
                if currency == 'ETH2':
                    currency = 'ethereum'
                price = convert_cryptocurrency(currency, float(account["balance"]["amount"]), 'gbp')
                self._coins[currency] = {}
                self._coins[currency]['balance'] = account["balance"]["amount"]
                if price is not None:
                    self._coins[currency]['gbp'] = round(price, 2)
                else:
                    self._coins[currency]['gbp'] = 0.0

