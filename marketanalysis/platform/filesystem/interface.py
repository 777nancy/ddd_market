from abc import ABC, abstractmethod

import pandas as pd


class AbstractFileSystem(ABC):
    @abstractmethod
    def write(self, df: pd.DataFrame, file_dir: str, file_name_base: str):
        raise NotImplementedError

    @abstractmethod
    def read(self, file_dir: str):
        raise NotImplementedError

    @abstractmethod
    def remove(self, file_dir: str):
        raise NotImplementedError
