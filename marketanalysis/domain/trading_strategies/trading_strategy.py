from abc import ABC, abstractmethod

import pandas as pd

from marketanalysis.domain.deal import Position
from marketanalysis.domain.indicators.indicator import AbstractIndicator


class AbstractTradingStrategy(ABC):
    @abstractmethod
    def trade(self, data: pd.DataFrame, indicator: AbstractIndicator) -> list[Position]:
        raise NotImplementedError
