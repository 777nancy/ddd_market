import pandas as pd

from marketanalysis.domain.deal import Position
from marketanalysis.domain.indicators.indicator import AbstractIndicator
from marketanalysis.domain.repository.interface import AbstractStockRepository
from marketanalysis.domain.ticker_symbol import TickerSymbol
from marketanalysis.domain.trading_strategies.trading_strategy import (
    AbstractTradingStrategy,
)


class Simulator(object):
    def __init__(
        self,
        indicator: AbstractIndicator,
        strategy: AbstractTradingStrategy,
        data: pd.DataFrame | None = None,
        ticker_symbol: TickerSymbol | None = None,
        stock_repository: AbstractStockRepository | None = None,
    ) -> None:
        if data is not None:
            self.data: pd.DataFrame = data
        elif ticker_symbol and stock_repository:
            self.data = stock_repository.select_to_df(ticker_symbol)
        else:
            raise
        self.indicator: AbstractIndicator = indicator
        self.strategy: AbstractTradingStrategy = strategy

        self.deals: list[Position] = []

    @property
    def profit(self):
        result = 0.0
        for deal in self.deals:
            result += deal.profit

        return result

    @property
    def total_return(self):
        buy_all = 0.0
        for deal in self.deals:
            buy_all += deal.buy_price
        if buy_all == 0.0:
            return 0.0
        return self.profit / buy_all

    def execute(self):
        self.deals = self.strategy.trade(self.data, self.indicator)

        return self.total_return, self.deals

    def from_new_data(self, ticker_symbol: TickerSymbol, stock_repository: AbstractStockRepository):
        return Simulator(self.indicator, self.strategy, ticker_symbol=ticker_symbol, stock_repository=stock_repository)
