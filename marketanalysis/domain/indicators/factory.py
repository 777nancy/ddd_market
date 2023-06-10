import importlib
import os

from marketanalysis.domain.indicators.indicator import AbstractIndicator
from marketanalysis.settings import constants


class IndicatorClassFactory(object):
    def create(self, indicator_name: str) -> type[AbstractIndicator]:
        module_name, class_name = indicator_name.split(".")
        module = importlib.import_module(f"{self._import_path_root()}.{module_name}")
        return getattr(module, class_name)

    @staticmethod
    def _import_path_root():
        abs_path_list = os.path.dirname(__file__).split("/")
        start_index = abs_path_list.index(constants.PROJECT_NAME)
        return ".".join(abs_path_list[start_index:])
