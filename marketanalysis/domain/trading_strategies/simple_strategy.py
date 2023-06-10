import pandas as pd

from marketanalysis.domain.deal import Position
from marketanalysis.domain.indicators.indicator import AbstractIndicator
from marketanalysis.domain.trading_strategies.trading_strategy import (
    AbstractTradingStrategy,
)


class SimpleTradingStrategy(AbstractTradingStrategy):
    @staticmethod
    def trade(data: pd.DataFrame, indicator: AbstractIndicator) -> list[Position]:
        deals: list[Position] = []
        positions: list[Position] = []
        buy_dates, sell_dates = indicator.signal()
        df = pd.concat(
            [
                pd.DataFrame({"date": buy_dates, "is_buy": True}),
                pd.DataFrame({"date": sell_dates, "is_sell": True}),
            ]
        )
        df = df.sort_values("date")
        df = df.merge(data, on=["date"], how="inner")[["date", "is_buy", "is_sell", "open"]]
        df = df.fillna({"is_buy": False, "is_sell": False})
        for row in df.itertuples():
            if not positions and row.is_buy:
                positions.append(Position.buy(row.open, row.date))

            elif positions and row.is_sell:
                for position in positions:
                    deals.append(position.sell(row.open, row.date))
                positions = []
        return deals


class SimpleTradingStrategyWithTradingStop(AbstractTradingStrategy):
    @staticmethod
    def trade(data: pd.DataFrame, indicator: AbstractIndicator, stop_limit: float = 0.2) -> list[Position]:
        deals: list[Position] = []
        positions: list[Position] = []
        buy_dates, sell_dates = indicator.signal()
        df = pd.concat(
            [
                pd.DataFrame({"date": buy_dates, "is_buy": True}),
                pd.DataFrame({"date": sell_dates, "is_sell": True}),
            ]
        )
        df = df.sort_values("date")
        df = df.merge(data, on=["date"], how="inner")[["date", "is_buy", "is_sell", "open", "low", "high"]]
        df = df.fillna({"is_buy": False, "is_sell": False})
        for row in df.itertuples():
            if not positions and row.is_buy:
                positions.append(Position.buy(row.open, row.date, row.open * (1 - stop_limit)))

            elif positions:
                update_position: list[Position] = []
                for position in positions:
                    if row.is_sell:
                        deals.append(position.sell(row.open, row.date))
                    elif position.should_sell_by_trading_stop(row.low):
                        deals.append(position.sell_trading_stop(row.date))
                    else:
                        update_position.append(position.update_trading_stop(row.high * (1 - stop_limit)))
                positions = update_position
        return deals
