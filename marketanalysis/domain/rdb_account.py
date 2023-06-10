from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class RDBAccount:
    user: str
    password: str
    host: str
    port: str | int
    database: str

    def connection_kwargs(self):
        base = {"user": self.user, "password": self.password, "host": self.host}

        for k, v in zip(["port", "database"], [str(self.port), self.database]):
            if len(v) > 0:
                base[k] = v
        return base

    @abstractmethod
    def connection_string(self):
        raise NotImplementedError


class PostgresqlAccount(RDBAccount):
    port: str | int = 5432

    def connection_string(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
