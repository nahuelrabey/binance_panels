import pandas as pd
import matplotlib.pyplot as plt

_oscilator_figsize = [15, 1.5]
_plot_figsize = [15, 4]


def emas(data: pd.DataFrame, ticks: list[int], path: str = None):
    """
    Plots the Exponential Moving Average (EMA) values for a given DataFrame and a list of specified periods.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock, and "{n}_ema" columns for each period in ticks, which represent the calculated EMA values.
    ticks (list[int]): A list of periods for which to plot the EMA. Each period represents the number of most recent closing prices that should be considered in the calculation.
    path (str, optional): The path where the plot should be saved. If not provided, the plot will be displayed using plt.show().

    Returns:
    None
    """
    plt.figure(1, figsize=_plot_figsize)

    x = data["datetime"]
    y = data["Close"]
    plt.plot(x, y)

    for tick in ticks:
        label = f"{tick}_ema"
        y = data[label]

        plt.plot(x, y, label=label)

    plt.legend()

    if (path != None):
        plt.savefig(path)
        plt.clf()
        return

    plt.show()
    return


def momentum(data: pd.DataFrame, tick: int):
    """
    Plots the momentum oscillator values for a given DataFrame and a specified period.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the stock data. It must include a "datetime" column, which represents the dates of the stock data, and a "{tick}_momentum" column, which represents the calculated momentum oscillator values.
    tick (int): The period for which to plot the momentum oscillator. This represents the number of most recent closing prices that should be considered in the calculation.

    Returns:
    None
    """
    plt.figure(1, figsize=_oscilator_figsize)
    x = data["datetime"]
    y = data[f"{tick}_momentum"]
    plt.plot(x, y)
    plt.plot(x, [1 for x in range(0, len(y))])
    plt.show()


def momentum_oscilators(data: pd.DataFrame, ticks: list[int]):
    """
    Plots the momentum oscillator values for a given DataFrame and a list of specified periods.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the stock data. It must include a "datetime" column, which represents the dates of the stock data, and "{n}_momentum" columns for each period in ticks, which represent the calculated momentum oscillator values.
    ticks (list[int]): A list of periods for which to plot the momentum oscillator. Each period represents the number of most recent closing prices that should be considered in the calculation.

    Returns:
    None
    """
    plt.figure(1, figsize=_oscilator_figsize)

    x = data["datetime"]

    plt.plot(x, [1 for x in range(0, len(x))], label="1",
             color="black", linestyle="dashed", linewidth=1, alpha=0.8)

    for tick in ticks:
        label = f"{tick}_momentum"
        y = data[label]
        plt.plot(x, y, label=label)

    plt.legend()
    plt.show()
    return
