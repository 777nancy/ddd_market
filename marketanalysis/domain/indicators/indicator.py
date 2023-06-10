import abc
from abc import abstractmethod

import pandas as pd
import pendulum


class AbstractIndicator(abc.ABC):
    # data: pd.DataFrame

    def get_params(self):
        raise NotImplementedError()

    @abstractmethod
    def calculate(self):
        raise NotImplementedError()

    @abstractmethod
    def signal(self):
        raise NotImplementedError()

    def should_buy_today(self):
        latest_date = self.data["date"].iloc[-1]  # type: ignore
        if str(latest_date) == pendulum.today(tz="Asia/Tokyo").strftime("%Y-%m-%d"):
            add_days = 0
        else:
            add_days = -1
        buy, _ = self.signal()
        print(self.get_params())
        if len(buy) == 0:
            return False
        today_str = pendulum.today(tz="Asia/Tokyo").add(days=add_days).strftime("%Y-%m-%d")
        if str(buy.iloc[-1]) == today_str:
            return True

        return False

    def should_sell_today(self):
        latest_date = self.data["date"].iloc[-1]  # type: ignore
        if str(latest_date) == pendulum.today(tz="Asia/Tokyo").strftime("%Y-%m-%d"):
            add_days = 0
        else:
            add_days = -1
        _, sell = self.signal()
        if len(sell) == 0:
            return False
        today_str = pendulum.today(tz="Asia/Tokyo").add(days=add_days).strftime("%Y-%m-%d")
        if str(sell.iloc[-1]) == today_str:
            return True

        return False

    @abstractmethod
    def draw(self, output_path=None, display_days=365):
        raise NotImplementedError()
