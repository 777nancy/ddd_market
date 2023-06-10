from dataclasses import dataclass
from enum import Enum

import pandas as pd


class MarketDataTableColumns(Enum):
    yyyymmdd = "yyyymmdd"
    date = "date"
    open = "open"
    high = "high"
    low = "low"
    close = "close"
    adj_close = "adj_close"
    volume = "volume"


@dataclass
class MarketDataTable:
    data: pd.DataFrame
    columns: MarketDataTableColumns = MarketDataTableColumns  # type: ignore
