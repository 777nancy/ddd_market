import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from marketanalysis.domain.indicators import indicator
from marketanalysis.utils import array


class Macd(indicator.AbstractIndicator):
    def __init__(self, data, short_period=12, long_period=26, signal_period=9):
        self.data: pd.DataFrame = data
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period
        self.calculate()

    def calculate(self):
        if self.short_period == self.long_period:
            self.data["MACD"] = 0
            self.data["Signal"] = 0

        # データの移動平均を計算
        self.data["ShortEMA"] = self.data["close"].ewm(span=self.short_period, adjust=False).mean()
        self.data["LongEMA"] = self.data["close"].ewm(span=self.long_period, adjust=False).mean()

        # MACDラインを計算
        self.data["MACD"] = self.data["ShortEMA"] - self.data["LongEMA"]

        # シグナルラインを計算
        self.data["Signal"] = self.data["MACD"].ewm(span=self.signal_period, adjust=False).mean()

        # MACDヒストグラムを計算
        self.data["Histogram"] = self.data["MACD"] - self.data["Signal"]

    def signal(self):
        buying_indexes, selling_indexes = array.intersection(
            self.data["MACD"],
            self.data["Signal"],
        )
        return self.data["date"].iloc[buying_indexes].reset_index(drop=True), self.data["date"].iloc[
            selling_indexes
        ].reset_index(drop=True)

    def get_params(self):
        return {
            "short_period": self.short_period,
            "long_period": self.long_period,
            "signal_period": self.signal_period,
        }

    def draw(self, output_path=None, display_days=365):
        data = self.data.copy()
        data["date"] = pd.to_datetime(data["date"])
        fig = plt.figure(linewidth=1, figsize=(16, 9))
        ax1, ax2 = fig.add_subplot(2, 1, 1), fig.add_subplot(2, 1, 2)
        columns_list = ["close", ["MACD", "Signal"]]
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

        fig.show()

        if output_path:
            fig.savefig(output_path)
