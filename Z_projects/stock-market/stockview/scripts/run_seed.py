import pandas as pd
from stockview.models import StockMarketData
from pathlib import Path
import json

import os
import random


def run():
    StockMarketData.objects.all().delete()

    # ROOT_PATH = Path(os.getcwd())
    # JSON_FILE_PATH = ROOT_PATH / 'stockview'/'stock_market_data.json'

    # # Read JSON file into DataFrame
    # df = pd.read_json(JSON_FILE_PATH)

    # # Convert date to datetime format
    # df['date'] = pd.to_datetime(df['date'])

    # # Convert numerical columns to appropriate data type and handle non-numeric values
    # numerical_columns = ['high', 'low', 'open', 'close', 'volume']
    # for col in numerical_columns:
    #     # Replace non-numeric values with NaN
    #     df[col] = pd.to_numeric(df[col], errors='coerce')

    # # Drop rows with invalid values (e.g., where 'volume' is 0)
    # df = df[df['volume'] != 0]

    # # Drop rows with missing values
    # df.dropna(inplace=True)

    # # df = df.sample(10)
    # print(f"Seeding {len(df)} records...")  # Seeding 1107 records...

    # # Seed the database with cleaned data
    # for index, row in df.iterrows():
    #     StockMarketData.objects.create(
    #         date=row['date'],
    #         trade_code=row['trade_code'],
    #         high=row['high'],
    #         low=row['low'],
    #         open=row['open'],
    #         close=row['close'],
    #         volume=row['volume']
    #     )
