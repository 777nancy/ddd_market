import logging
import re
from pathlib import Path

import yaml

from marketanalysis.domain.ticker_symbol import TickerSymbol
from marketanalysis.settings import constants

logger = logging.getLogger(__name__)


class ParametersManager(object):
    def __init__(self) -> None:
        param_config_path = Path(constants.CONFIG_DIR, "parameters.yml")

        with param_config_path.open() as fin:
            self.param_config = yaml.safe_load(fin)

    def get_params(self, indicator_name, param_name=None):
        def format(config):
            config[0].pop("name")
            config[0].pop("default")
            result = config[0]
            buffer = self._buffer(result)
            result = self._to_list(result)
            result["data_period"] = self.param_config.get(indicator_name).get("data_period")
            result["buffer"] = buffer

            return result

        target_config = self.param_config.get(indicator_name).get("params")
        if len(target_config) == 1:
            return format(target_config)

        else:
            for target in target_config:
                if (target.get("name") == param_name) or (target.get("default") is True):
                    return format(target_config)
            logger.warning(f"param_name {param_name} does not exit")
            return

    @staticmethod
    def _to_list(target_config):
        formatted_config = {}
        for k, v in target_config.items():
            formatted_config[k] = [i for i in range(v.get("min", 0), v.get("max", 0) + 1)]
        return formatted_config

    @staticmethod
    def _buffer(target_config):
        max_days = 0
        for v in target_config.values():
            max_days = max(v.get("max", 0), max_days)
        return max_days


class TickerSymbolsManager(object):
    def __init__(self) -> None:
        ticker_config_path = Path(constants.CONFIG_DIR, "ticker_symbols.yml")

        with ticker_config_path.open() as fin:
            self.ticker_config = yaml.safe_load(fin)

    def get_all(self) -> list[TickerSymbol]:
        ticker_symbols = []

        for ticker_info in self.ticker_config.get("ticker_symbols"):
            ticker_symbols.append(TickerSymbol(**ticker_info))
        return ticker_symbols

    def get(self, ticker_symbol: str) -> TickerSymbol:
        for ticker_info in self.ticker_config.get("ticker_symbols"):
            if ticker_info.get("ticker_symbol") == ticker_symbol:
                return TickerSymbol(**ticker_info)
        logger.warning(f"ticker symbol {ticker_symbol} does not exit in config")
        return TickerSymbol(
            ticker_symbol=ticker_symbol, name=self._clean(ticker_symbol), short_name=self._clean(ticker_symbol)
        )

    @staticmethod
    def _clean(text):
        code_regex = re.compile("[!\"#$%&'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]")

        striped_text = text.strip()
        cleaned_text = code_regex.sub("", striped_text)
        return cleaned_text
