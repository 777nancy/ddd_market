import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TickerSymbol:
    ticker_symbol: str
    name: str
    short_name: str

    @property
    def table_name(self):
        return f"stock_price_{self.short_name}".lower()
