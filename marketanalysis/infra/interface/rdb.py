from abc import ABC, abstractmethod

import pandas as pd

from marketanalysis.domain.query import Query


class RDB(ABC):
    @abstractmethod
    def select_to_df(self, query: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def update_by_df(self, df: pd.DataFrame, table_name: str):
        raise NotImplementedError

    @abstractmethod
    def execute(self, query: str | Query, need_fetch: bool = True):
        raise NotImplementedError
