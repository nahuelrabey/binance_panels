import pandas as pd
import matplotlib.pyplot as plt

_oscilator_figsize = [15, 1.5]
_plot_figsize = [15, 4]


def plot_emas(data: pd.DataFrame, ticks: 'list[int]', path: str = None):
    plt.figure(1, figsize=_plot_figsize)

    x = data["datetime"]
    y = data["Close"]
    plt.plot(x, y)

    for tick in ticks:
        # plt.figure()
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


def plot_momentum(data: pd.DataFrame, tick: int):
    plt.figure(1, figsize=_oscilator_figsize)
    x = data["datetime"]
    y = data[f"{tick}_momentum"]
    plt.plot(x, y)
    plt.plot(x, [1 for x in range(0, len(y))])
    plt.show()


def plot_momentum_oscilators(data: pd.DataFrame, ticks: list[int]):
    # plt.figure(1, figsize=[15,4])
    # x = data["datetime"]
    # y = data[f"{tick}_momentum"]
    # plt.plot(x,y)
    # plt.plot(x,[1 for x in range(0,len(y))])
    # plt.show()
    plt.figure(1, figsize=_oscilator_figsize)

    x = data["datetime"]

    plt.plot(x, [1 for x in range(0, len(x))], label="1",
             color="black", linestyle="dashed", linewidth=1, alpha=0.8)

    for tick in ticks:
        # plt.figure()
        label = f"{tick}_momentum"
        y = data[label]
        plt.plot(x, y, label=label)


    plt.legend()
    plt.show()
    return
