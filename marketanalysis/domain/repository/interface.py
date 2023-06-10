from abc import ABC, abstractmethod

import pandas as pd

from marketanalysis.domain.slack_message import SlackMessage
from marketanalysis.domain.ticker_symbol import TickerSymbol


class AbstractStockRepository(ABC):
    @abstractmethod
    def create_or_update(self, ticker_symbol: TickerSymbol):
        raise NotImplementedError

    @abstractmethod
    def select_to_df(self, ticker_symbol: TickerSymbol) -> pd.DataFrame:
        raise NotImplementedError


class AbstractSlackNotificationRepository(ABC):
    def notify(self, comment: SlackMessage, file_uploads_data: list[dict] | None = None):
        raise NotImplementedError
