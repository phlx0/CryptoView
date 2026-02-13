import requests
from models.coin import Coin
from typing import List, Optional

class CryptoService:
    BASE_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    def get_top_coins(vs_currency: str = "usd", per_page: int = 100) -> Optional[List[Coin]]:
        url = f"{CryptoService.BASE_URL}/coins/markets"
        params = {"vs_currency": vs_currency, "order": "market_cap_desc", "per_page": per_page, "page": 1}
        r = requests.get(url, params=params)
        if r.status_code != 200:
            return None
        data = r.json()
        if not isinstance(data, list):
            return None
        return [Coin.from_api(c) for c in data]

    @staticmethod
    def get_ohlc_history(coin_id: str, vs_currency: str = "usd", days: int = 7):
        url = f"{CryptoService.BASE_URL}/coins/{coin_id}/ohlc"
        r = requests.get(url, params={"vs_currency": vs_currency, "days": days})
        if r.status_code != 200:
            return None
        return r.json()
    