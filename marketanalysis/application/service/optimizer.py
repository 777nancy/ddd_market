import inspect
import itertools
import logging
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
from tqdm import tqdm

from marketanalysis.application.service.simulator import Simulator
from marketanalysis.domain.indicators.indicator import AbstractIndicator
from marketanalysis.domain.repository.interface import AbstractStockRepository
from marketanalysis.domain.ticker_symbol import TickerSymbol
from marketanalysis.domain.trading_strategies.trading_strategy import (
    AbstractTradingStrategy,
)

logger = logging.getLogger(__name__)


class Optimizer(object):
    def __init__(
        self,
        ticker_symbol: TickerSymbol,
        indicator_class: type[AbstractIndicator],
        strategy_class: type[AbstractTradingStrategy],
        stock_repository: AbstractStockRepository,
    ) -> None:
        self.ticker_symbol = ticker_symbol
        self.indicator_class = indicator_class
        self.strategy_class = strategy_class
        self.stock_repository = stock_repository

    def _select(self) -> pd.DataFrame:
        return self.stock_repository.select_to_df(self.ticker_symbol)

    def execute(self, params):
        arg_names = inspect.getargspec(self.indicator_class).args
        l: list[list] = []
        for arg_name in arg_names:
            if params.get(arg_name):
                l.append(params.get(arg_name))
        products = itertools.product(*l)
        data = self._select()
        data_period = params.get("data_period", 365) + params.get("buffer", 0)
        data = data[-data_period:]
        with tqdm(total=len(list(itertools.product(*l)))) as pbar:
            with ProcessPoolExecutor(2) as executor:
                indicator_objects = [self.indicator_class(data.copy(), *product) for product in list(products)]  # type: ignore
                simulators = [
                    Simulator(indicator_object, self.strategy_class(), data.copy())
                    for indicator_object in indicator_objects
                ]
                features = [executor.submit(simulator.execute) for simulator in simulators]
                [feature.add_done_callback(lambda p: pbar.update()) for feature in features]
                result = []
                for indicator_object, simulator, feature in zip(indicator_objects, simulators, features):
                    total_return, deals = feature.result()
                    result.append(
                        {
                            "total_return": total_return,
                            "params": indicator_object.get_params(),
                            "indicator": indicator_object,
                            "simulator": simulator,
                            "deals": deals,
                        }
                    )
        sorted_result = sorted(result, key=lambda x: x["total_return"])
        return sorted_result[-1]
