import argparse
import logging
from logging import INFO, basicConfig

from marketanalysis.application.optimize import Optimize
from marketanalysis.application.stock_update import StockUpdate
from marketanalysis.domain.rdb_account import PostgresqlAccount
from marketanalysis.infra.postgresql import Postgresql
from marketanalysis.infra.slack_notification_repository import (
    SlackNotificationRepository,
)
from marketanalysis.infra.stock_repository import StockRepository
from marketanalysis.settings.constants import (
    POSTGRES_DATABASE,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

logger = logging.getLogger(__name__)


def stock_update(args):
    logger.info(f"ticker_symbol: {args.ticker_symbol}")
    usecase = StockUpdate(
        StockRepository(
            Postgresql(
                PostgresqlAccount(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE)
            )
        ),
        SlackNotificationRepository(),
    )

    usecase.execute(args.ticker_symbol)


def optimize(args):
    logger.info(f"indicator: {args.indicator}")
    logger.info(f"params: {args.param}")
    logger.info(f"optimized_ticker_symbol: {args.optimized_ticker_symbol}")
    logger.info(f"strategy: {args.strategy}")
    logger.info(f"target_ticker_symbol: {args.target_ticker_symbol}")
    usecase = Optimize(
        StockRepository(
            Postgresql(
                PostgresqlAccount(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE)
            )
        ),
        SlackNotificationRepository(),
    )
    usecase.execute(args.indicator, args.param, args.optimized_ticker_symbol, args.strategy, args.target_ticker_symbol)


if __name__ == "__main__":
    basicConfig(level=INFO, format="{asctime} [{levelname:.4}] {name}: {message}", style="{")
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # stock update
    subparser_stock_update = subparsers.add_parser("stock_update", description="update stock data")
    subparser_stock_update.add_argument("-t", "--ticker-symbol", nargs="*", type=str, default=None)
    subparser_stock_update.set_defaults(func=stock_update)

    # optimize
    subparser_optimize = subparsers.add_parser("optimize", description="optimize indicator")
    subparser_optimize.add_argument("-i", "--indicator", type=str, required=True)
    subparser_optimize.add_argument("-p", "--param", type=str, default="default")
    subparser_optimize.add_argument("-ot", "--optimized-ticker-symbol", type=str, required=True)
    subparser_optimize.add_argument("-tt", "--target-ticker-symbol", type=str, default=None)
    subparser_optimize.add_argument(
        "-s", "--strategy", type=str, default="simple_strategy.SimpleTradingStrategyWithTradingStop"
    )

    subparser_optimize.set_defaults(func=optimize)

    args = parser.parse_args()

    args.func(args)
