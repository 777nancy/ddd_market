import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from marketanalysis.domain.indicators import indicator
from marketanalysis.utils import array


class Stochastic(indicator.AbstractIndicator):
    def __init__(self, data, k_period=14, d_period=3, overbought=80, oversold=20):
        self.data: pd.DataFrame = data
        self.k_period = k_period
        self.d_period = d_period
        self.overbought = overbought
        self.oversold = oversold
        self.calculate()

    def calculate(self):
        # 最高値と最安値の範囲を計算
        self.data["overbought"] = self.overbought
        self.data["oversold"] = self.oversold
        self.data["high_max"] = self.data["high"].rolling(window=self.k_period, min_periods=1).max()
        self.data["low_min"] = self.data["low"].rolling(window=self.k_period, min_periods=1).min()

        # %Kの計算
        self.data["%K"] = (
            (self.data["close"] - self.data["low_min"]) / (self.data["high_max"] - self.data["low_min"]) * 100
        )

        # %Dの計算
        self.data["%D"] = self.data["%K"].rolling(window=self.d_period, min_periods=1).mean()

    def signal(self):
        buying_indexes, selling_indexes = array.intersection_with_bounds(
            self.data["%D"], self.data["%K"], self.oversold, self.oversold
        )
        return self.data["date"].iloc[buying_indexes].reset_index(drop=True), self.data["date"].iloc[
            selling_indexes
        ].reset_index(drop=True)

    def get_params(self):
        return {
            "k_period": self.k_period,
            "d_period": self.d_period,
            "overbought": self.overbought,
            "oversold": self.oversold,
        }

    def draw(self, output_path=None, display_days=365):
        data = self.data.copy()
        data["date"] = pd.to_datetime(data["date"])
        fig = plt.figure(linewidth=1, figsize=(16, 9))

        ax1, ax2 = fig.add_subplot(2, 1, 1), fig.add_subplot(2, 1, 2)
        columns_list = ["close", ["%K", "%D", "overbought", "oversold"]]
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


class SlowStochastic(Stochastic):
    def __init__(self, data, k_period=14, d_period=3, overbought=80, oversold=20, slow_period=3):
        self.slow_period = slow_period
        super().__init__(data, k_period, d_period, overbought, oversold)

    def calculate(self):
        super().calculate()
        self.data["slow_%K"] = self.data["%D"]
        self.data["slow_%D"] = self.data["slow_%K"].rolling(window=self.slow_period, min_periods=1).mean()

    def signal(self):
        buying_indexes, selling_indexes = array.intersection_with_bounds(
            self.data["slow_%D"].reset_index(drop=True),
            self.data["slow_%K"].reset_index(drop=True),
            self.oversold,
            self.oversold,
        )
        return self.data["date"].iloc[buying_indexes].reset_index(drop=True), self.data["date"].iloc[
            selling_indexes
        ].reset_index(drop=True)

    def get_params(self):
        return {
            "k_period": self.k_period,
            "d_period": self.d_period,
            "slow_period": self.k_period,
            "overbought": self.overbought,
            "oversold": self.oversold,
        }

    def draw(self, output_path=None, display_days=365):
        data = self.data.copy()
        data["date"] = pd.to_datetime(data["date"])
        fig = plt.figure(linewidth=1, figsize=(16, 9))

        ax1, ax2 = fig.add_subplot(2, 1, 1), fig.add_subplot(2, 1, 2)
        columns_list = ["close", ["slow_%K", "slow_%D", "overbought", "oversold"]]
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
