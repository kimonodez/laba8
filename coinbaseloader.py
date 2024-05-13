import json
from datetime import datetime
import requests
import pandas as pd
from baseloader import BaseDataLoader
from enum import Enum

class Granularity(Enum):
    ONE_MINUTE = 60
    FIVE_MINUTES = 300
    FIFTEEN_MINUTES = 900
    ONE_HOUR = 3600
    SIX_HOURS = 21600
    ONE_DAY = 86400

class CoinbaseLoader(BaseDataLoader):
    """
    Клас для завантаження даних з біржі Coinbase через їх API.
    """

    def __init__(self, endpoint="https://api.exchange.coinbase.com"):
        """
        Ініціалізує клас CoinbaseLoader з вказаним API-кінцевим пунктом.

        Args:
        - endpoint (str): Базова URL-адреса API біржі Coinbase.
        """
        super().__init__(endpoint)

    def get_pairs(self) -> pd.DataFrame:
        """
        Отримання DataFrame доступних торгових пар на біржі Coinbase.

        Returns:
        - pd.DataFrame: DataFrame
        """
        data = self._get_req("/products")
        df = pd.DataFrame(json.loads(data))
        df.set_index('id', drop=True, inplace=True)
        return df

    def get_stats(self, pair: str) -> pd.DataFrame:
        """
     статистика для торгової пари на Coinbase.

        Args:
        - pair (str): Торгова пара, для якої потрібно отримати статистику.

        Returns:
        - pd.DataFrame: DataFrame, якй містить статистику для торгової пари.
        """
        data = self._get_req(f"/products/{pair}")
        return pd.DataFrame(json.loads(data), index=[0])

    def get_historical_data(self, pair: str, begin: datetime, end: datetime, granularity: Granularity) -> pd.DataFrame:
        """
        Отримання дані цін для торгової пари на Coinbase.

        Args:
        - pair (str): Торгова пара, для якої потрібно отримати історичні дані.
        - begin (datetime): Початкова дата історичних даних.
        - end (datetime): Кінцева дата історичних даних.
        - granularity (Granularity): Гранулярка даних.

        Returns:
        - pd.DataFrame: DataFrame
        """
        params = {
            "start": begin.strftime('%Y-%m-%d'),
            "end": end.strftime('%Y-%m-%d'),
            "granularity": granularity.value
        }
        # Отримання потрібних даних з біржі Coinbase
        data = self._get_req(f"/products/{pair}/candles", params)
        # Парсинг відповідtq та створення DataFrame
        df = pd.DataFrame(json.loads(data),
                          columns=("timestamp", "low", "high", "open", "close", "volume"))
        # Використання стовпця з часом як індекс
        df.set_index('timestamp', drop=True, inplace=True)
        return df

if __name__ == "__main__":
    loader = CoinbaseLoader()
    data = loader.get_pairs()
    print(data)
    data = loader.get_stats("btc-usdt")
    print(data)
    data = loader.get_historical_data("btc-usdt", datetime(2023, 1, 1), datetime(2023, 6, 30), granularity=Granularity.ONE_DAY)
    print(data.head(5))
