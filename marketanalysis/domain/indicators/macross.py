import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from marketanalysis.domain.indicators import indicator
from marketanalysis.utils import array


class EmaCross(indicator.AbstractIndicator):
    def __init__(self, data, short_period=12, long_period=26):
        self.data: pd.DataFrame = data
        self.short_period = short_period
        self.long_period = long_period
        self.calculate()

    def calculate(self):
        # データの移動平均を計算
        self.data["short_ema"] = self.data["close"].ewm(span=self.short_period, adjust=False).mean()
        self.data["long_ema"] = self.data["close"].ewm(span=self.long_period, adjust=False).mean()

    def signal(self):
        """_summary_

        Returns:
            tuple[ndarray[int], ndarray[int]]: buy, sellのインデックス
        """

        buying_indexes, selling_indexes = array.intersection(
            self.data["long_ema"],
            self.data["short_ema"],
        )
        return self.data["date"].iloc[buying_indexes].reset_index(drop=True), self.data["date"].iloc[
            selling_indexes
        ].reset_index(drop=True)

    def get_params(self):
        return {"short_period": self.short_period, "long_period": self.long_period}

    def draw(self, output_path=None, display_days=365):
        data = self.data.copy()
        data["date"] = pd.to_datetime(data["date"])
        plt.figure(linewidth=1, figsize=(16, 9))
        target_columns = ["short_ema", "long_ema", "close"]
        plt.plot(
            data["date"][-display_days:],
            data[target_columns][-display_days:],
            label=target_columns,
        )
        plt.xticks(rotation=60)
        locator = mdates.MonthLocator()
        plt.gca().xaxis.set_major_locator(locator)
        plt.legend()
        plt.show()
        if output_path:
            plt.savefig(output_path)
