import logging
import os

import pandas as pd
import yfinance

from marketanalysis.domain.query import Query
from marketanalysis.domain.repository.interface import AbstractStockRepository
from marketanalysis.domain.ticker_symbol import TickerSymbol
from marketanalysis.infra.interface.rdb import RDB
from marketanalysis.platform.filesystem.interface import AbstractFileSystem
from marketanalysis.settings import PROJECT_BUCKET_NAME, RESOURCES_DIR

logger = logging.getLogger(__name__)


class StockRepository(AbstractStockRepository):
    def __init__(self, rdb: RDB) -> None:
        self.rdb: RDB = rdb

    def select_to_df(self, ticker_symbol: TickerSymbol) -> pd.DataFrame:
        query = f"select * from {ticker_symbol.table_name} order by yyyymmdd"
        return self.rdb.select_to_df(query)

    def create_or_update(self, ticker_symbol: TickerSymbol):
        latest_date = None
        self.rdb.execute(f"drop table if exists {ticker_symbol.table_name}", need_fetch=False)
        # if not table_exits:
        logger.info(f"table {ticker_symbol.table_name} does not exit")
        query = Query.from_file(
            os.path.join(RESOURCES_DIR, "stock_table.sql"), {"table_name": ticker_symbol.table_name}
        )

        self.rdb.execute(query.format(), need_fetch=False)

        latest_date = None
        # else:
        #     _start_date = self.rdb.execute(
        #         f"SELECT yyyymmdd FROM {ticker_symbol.table_name} ORDER BY yyyymmdd desc LIMIT 1", need_fetch=True
        #     )
        #     latest_date = _start_date[0][0] if _start_date else None

        #     latest_date = pendulum.from_format(str(latest_date), "YYYYMMDD").add(days=-1)

        stock_df = yfinance.download(ticker_symbol.ticker_symbol, start=latest_date).reset_index()
        if len(stock_df) == 0:
            logger.info(f"stock price data({ticker_symbol.short_name}) is up to date")
            return
        stock_df = stock_df.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            }
        )
        stock_df["yyyymmdd"] = stock_df["date"].astype(str).str.replace("-", "")
        self.rdb.update_by_df(stock_df, ticker_symbol.table_name)

    def _table_exists(self, ticker_symbol: TickerSymbol) -> bool:
        query = f"select count(*) from pg_tables where tablename='{ticker_symbol.table_name}'"

        rows = self.rdb.execute(query, need_fetch=True)
        return True if rows[0][0] else False


class FileStockRepository(AbstractStockRepository):
    def __init__(self, filesystem: AbstractFileSystem) -> None:
        self.filesystem = filesystem

    def select_to_df(self, ticker_symbol: TickerSymbol) -> pd.DataFrame:
        file_dir = f"{PROJECT_BUCKET_NAME}/{ticker_symbol.short_name}"

        return self.filesystem.read(file_dir)

    def create_or_update(self, ticker_symbol: TickerSymbol):
        file_dir = f"{PROJECT_BUCKET_NAME}/{ticker_symbol.short_name}"

        stock_df = yfinance.download(ticker_symbol.ticker_symbol).reset_index()
        if len(stock_df) == 0:
            logger.info(f"stock price data({ticker_symbol.short_name}) is up to date")
            return
        stock_df = stock_df.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            }
        )
        stock_df["yyyymmdd"] = stock_df["date"].astype(str).str.replace("-", "")
        self.filesystem.write(stock_df, file_dir, ticker_symbol.short_name)
