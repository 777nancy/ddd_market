import logging

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from marketanalysis.domain.query import Query
from marketanalysis.domain.rdb_account import RDBAccount
from marketanalysis.infra.interface.rdb import RDB

logger = logging.getLogger(__name__)


class Postgresql(RDB):
    def __init__(self, postgresql_account: RDBAccount) -> None:
        self.connection_config = postgresql_account.connection_kwargs()

        self.engine = create_engine(postgresql_account.connection_string())

    def select_to_df(self, query: str) -> pd.DataFrame:
        return pd.read_sql(query, self.engine)

    def update_by_df(self, df: pd.DataFrame, table_name: str):
        df.to_sql(table_name, self.engine, if_exists="append", index=False)

    def execute(self, query: str | Query, need_fetch: bool = True):
        _query = query
        if query is Query:
            _query = query.format()

        connection = psycopg2.connect(**self.connection_config)
        with psycopg2.connect(**self.connection_config) as connection:
            with connection.cursor() as cur:
                logger.info("query is executed")
                logger.info(_query)

                cur.execute(_query)  # type: ignore

                logger.info("query is successful")

                if need_fetch:
                    return cur.fetchall()
