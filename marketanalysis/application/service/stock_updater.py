import logging

from marketanalysis.domain.config import TickerSymbolsManager
from marketanalysis.domain.repository.interface import AbstractStockRepository
from marketanalysis.domain.ticker_symbol import TickerSymbol

logger = logging.getLogger(__name__)


class StockUpdater(object):
    def __init__(self, stock_repository: AbstractStockRepository) -> None:
        self.stock_repository = stock_repository

    def execute(self, ticker_symbol: str | TickerSymbol | None = None):
        logger.info("START: ticker symbol update")
        ticker_symbols_manager = TickerSymbolsManager()
        ticker_symbol_list: list[TickerSymbol] = []
        if ticker_symbol:
            ticker_symbol_list = (
                [ticker_symbols_manager.get(ticker_symbol)] if ticker_symbol is str else [ticker_symbol]  # type: ignore
            )
        else:
            ticker_symbol_list = ticker_symbols_manager.get_all()

        for ticker in ticker_symbol_list:
            logger.info(f"START: ticker symbol {ticker.short_name} update")
            self.stock_repository.create_or_update(ticker)
            logger.info(f"END: ticker symbol {ticker.short_name} update")

        logger.info("END: ticker symbol update")
