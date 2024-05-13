import pytest
from unittest.mock import patch
from coinbaseloader import CoinbaseLoader, Granularity
import pandas as pd
from datetime import datetime

@pytest.fixture
def loader():
    return CoinbaseLoader()

@pytest.mark.parametrize("pair, begin, end, granularity, expected_shape", [
    ("btc-usdt", datetime(2023, 1, 1), datetime(2023, 1, 2), Granularity.ONE_DAY, (1, 6)),
    # Додайте інші варіанти тестів тут
])
@patch('coinbaseloader.BaseDataLoader._get_req')
def test_get_historical_data(mock_get_req, loader):
    # Arrange
    pair = "btc-usdt"
    begin = datetime(2023, 1, 1)
    end = datetime(2023, 1, 2)
    granularity = Granularity.ONE_DAY
    mock_get_req.return_value = '[[1514764800, 100, 200, 150, 180, 1000]]'

    # Act
    df = loader.get_historical_data(pair, begin, end, granularity)

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 6)  # Перевірка на розмір DataFrame

