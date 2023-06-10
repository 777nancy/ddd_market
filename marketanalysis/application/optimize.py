import logging
import os
import tempfile

from marketanalysis.application.service.optimizer import Optimizer
from marketanalysis.application.service.simulator import Simulator
from marketanalysis.domain.config import ParametersManager, TickerSymbolsManager
from marketanalysis.domain.indicators.factory import IndicatorClassFactory
from marketanalysis.domain.indicators.indicator import AbstractIndicator
from marketanalysis.domain.repository.interface import AbstractStockRepository
from marketanalysis.domain.slack_message import SlackMessage
from marketanalysis.domain.trading_strategies.factory import TradingStrategyClassFactory
from marketanalysis.infra.slack_notification_repository import (
    SlackNotificationRepository,
)
from marketanalysis.settings.constants import RESOURCES_DIR

logger = logging.getLogger(__name__)


class Optimize(object):
    def __init__(self, stock_repository: AbstractStockRepository, slack: SlackNotificationRepository) -> None:
        self.stock_repository = stock_repository
        self.slack = slack

    def execute(self, indicator, param, optimized_ticker_symbol, strategy, target_ticker_symbol):
        ticker = TickerSymbolsManager().get(optimized_ticker_symbol)

        indicator_class = IndicatorClassFactory().create(indicator)
        strategy_class = TradingStrategyClassFactory().create(strategy)
        optimizer = Optimizer(ticker, indicator_class, strategy_class, self.stock_repository)

        params = ParametersManager().get_params(indicator.split(".")[-1], param)

        optimized_params = optimizer.execute(params)
        optimized_indicator: AbstractIndicator = optimized_params.pop("indicator")
        simulator: Simulator = optimized_params.pop("simulator")

        placeholder = {
            "optimized_ticker_short_name": ticker.short_name,
            "optimized_indicator_name": indicator,
            "optimized_total_return": optimized_params.get("total_return"),
            "optimized_params": optimized_params.get("params"),
            "optimized_should_buy": optimized_indicator.should_buy_today(),
            "optimized_should_sell": optimized_indicator.should_sell_today(),
        }
        png_files = []
        png_path = os.path.join(tempfile.mkdtemp(), "{ticker.short_name}.png")
        optimized_indicator.draw(png_path)
        png_files.append({"title": ticker.short_name, "file": png_path})

        if target_ticker_symbol:
            target_ticker = TickerSymbolsManager().get(target_ticker_symbol)
            target_simulator = simulator.from_new_data(target_ticker, self.stock_repository)
            target_simulator.execute()

            placeholder = {
                **{
                    "has_target_ticker": True if target_ticker_symbol else False,
                    "target_ticker_short_name": target_ticker.short_name,
                    "target_total_return": target_simulator.total_return,
                    "target_should_buy": target_simulator.indicator.should_buy_today(),
                    "target_should_sell": target_simulator.indicator.should_sell_today(),
                },
                **placeholder,
            }
            png_path = os.path.join(tempfile.mkdtemp(), "{target_ticker.short_name}.png")
            optimized_indicator.draw(png_path)
            png_files.append({"title": target_ticker.short_name, "file": png_path})

        message = SlackMessage.from_file(os.path.join(RESOURCES_DIR, "message.txt"), placeholder)
        self.slack.notify(message, png_files)
