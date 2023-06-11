import abc
from abc import abstractmethod

import pandas as pd
import pendulum


class AbstractIndicator(abc.ABC):
    _data: pd.DataFrame

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @abstractmethod
    def get_params(self, data):
        raise NotImplementedError()

    @abstractmethod
    def calculate(self):
        raise NotImplementedError()

    @abstractmethod
    def get_indexes(self):
        raise NotImplementedError()

    @abstractmethod
    def signal(self):
        raise NotImplementedError()

    def should_buy_today(self):
        buying_indexes, _ = self.get_indexes()
        if len(buying_indexes) == 0:
            return False

        try:
            self.data["date"].iloc[buying_indexes + 1].reset_index(drop=True)
            return False
        except IndexError:
            return True

    def should_sell_today(self):
        _, selling_indexes = self.get_indexes()
        if len(selling_indexes) == 0:
            return False

        try:
            self.data["date"].iloc[selling_indexes + 1].reset_index(drop=True)
            return False
        except IndexError:
            return True

    @abstractmethod
    def draw(self, output_path=None, display_days=365):
        raise NotImplementedError()
