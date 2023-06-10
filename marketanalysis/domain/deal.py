from dataclasses import dataclass, field


@dataclass
class Position(object):
    buy_price: float
    buy_date: str
    trading_stop_price: float = field(default=0)
    sell_price: float = field(default=0)
    sell_date: str = field(default="")
    trading_stop: bool = field(default=False)

    @property
    def profit(self) -> float:
        return self.sell_price - self.buy_price

    def sell(self, sell_price, sell_date):
        return Position(
            buy_price=self.buy_price,
            buy_date=self.buy_date,
            trading_stop_price=self.trading_stop_price,
            sell_price=sell_price,
            sell_date=sell_date,
        )

    def sell_trading_stop(self, sell_date):
        return Position(
            buy_price=self.buy_price,
            buy_date=self.buy_date,
            trading_stop_price=self.trading_stop_price,
            sell_price=self.trading_stop_price,
            sell_date=sell_date,
            trading_stop=True,
        )

    @classmethod
    def buy(cls, buy_price, buy_date, trading_stop_price=0):
        return cls(buy_price=buy_price, buy_date=buy_date, trading_stop_price=trading_stop_price)

    def update_trading_stop(self, trading_stop_price):
        if self.trading_stop_price < trading_stop_price:
            return Position(
                buy_price=self.buy_price,
                buy_date=self.buy_date,
                trading_stop_price=trading_stop_price,
            )
        return self

    def should_sell_by_trading_stop(self, low):
        if self.trading_stop_price < low:
            return True

        return False
