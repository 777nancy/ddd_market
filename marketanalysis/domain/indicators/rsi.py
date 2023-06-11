import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from marketanalysis.domain.indicators.indicator import AbstractIndicator
from marketanalysis.utils import array


class Rsi(AbstractIndicator):
    def __init__(self, data, period=14, overbought=70, oversold=30):
        self._data: pd.DataFrame = data
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.calculate()

    def calculate(self):
        # 終値の変化量を求める
        self.data["overbought"] = self.overbought
        self.data["oversold"] = self.oversold
        delta = self.data["close"].diff()

        # 上昇幅と下降幅を求める
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # 上昇幅と下降幅の平均を求める
        avg_gain = gain.rolling(self.period, min_periods=1).mean()
        avg_loss = loss.rolling(self.period, min_periods=1).mean()

        # RSIを計算する
        self.data["rsi"] = np.where(avg_loss == 0, 100, 100 - (100 / (1 + avg_gain / avg_loss)))

    def get_indexes(self):
        buying_indexes, _ = array.intersection(self.data["oversold"], self.data["rsi"])
        _, selling_indexes = array.intersection(self.data["overbought"], self.data["rsi"])

        return buying_indexes, selling_indexes

    def signal(self):
        buying_indexes, selling_indexes = self.get_indexes()
        buying_indexes = buying_indexes[:-1]
        selling_indexes = selling_indexes[:-1]
        return self.data["date"].iloc[buying_indexes + 1].reset_index(drop=True), self.data["date"].iloc[  # type: ignore
            selling_indexes + 1
        ].reset_index(
            drop=True
        )

    def get_params(self):
        return {
            "period": self.period,
            "overbought": self.overbought,
            "oversold": self.oversold,
        }

    def draw(self, output_path=None, display_days=365):
        data = self.data.copy()
        data["date"] = pd.to_datetime(data["date"])
        fig = plt.figure(linewidth=1, figsize=(16, 9))

        ax1, ax2 = fig.add_subplot(2, 1, 1), fig.add_subplot(2, 1, 2)
        columns_list = ["close", ["rsi", "overbought", "oversold"]]
        locator = mdates.MonthLocator()
        for ax, columns in zip([ax1, ax2], columns_list):  # type: ignore
            ax.plot(
                data["date"][-display_days:],
                data[columns][-display_days:],
                label=columns,
            )
            ax.legend(loc="upper left")
        ax1.tick_params(labelbottom=False, bottom=False)
        ax2.xaxis.set_tick_params(rotation=60)
        ax2.xaxis.set_major_locator(locator)

        plt.show()
        if output_path:
            plt.savefig(output_path)
