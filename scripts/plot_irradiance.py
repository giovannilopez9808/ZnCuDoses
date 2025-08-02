from matplotlib import pyplot
from os.path import join
from typing import List
from pandas import (
    DataFrame,
    Timestamp,
    read_csv,
    to_datetime,
)


def get_dates(
    data: DataFrame,
) -> List[Timestamp]:
    dates = sorted(
        set(
            data.index.date
        )
    )
    return dates


filename = join(
    "..",
    "data",
    "data.csv",
)
dataset = read_csv(
    filename,
    index_col="Nombre",
)
for name in dataset.index:
    folder = join(
        "..",
        "results",
        "TUV",
    )
    filename = f"{name}.csv"
    filename = join(
        folder,
        filename,
    )
    radiation = read_csv(
        filename,
        parse_dates=True,
        index_col=0,
    )
    radiation.index = list(
        date.replace(
            day=date.month,
            month=1,
        )
        for date in radiation.index
    )
    radiation = radiation.resample(
        "1min"
    ).mean()
    ticks = get_dates(
        radiation,
    )
    dates = list(
        to_datetime(
            f"{tick} 15:00"
        )
        for tick in ticks
    )
    pyplot.subplots(
        figsize=(
            16,
            5,
        )
    )
    pyplot.ylim(
        0,
        0.6,
    )
    pyplot.plot(
        radiation["zn"],
        label="Zn",
    )
    pyplot.plot(
        radiation["cu"],
        label="Cu",
    )
    pyplot.xticks(
        dates,
        ticks,
    )
    pyplot.tick_params(
        labelsize=13,
    )
    pyplot.legend(
        fontsize=16,
    )
    folder = join(
        "..",
        "graphics",
        "TUV"
    )
    filename = f"{name}.png"
    filename = join(
        folder,
        filename,
    )
    pyplot.savefig(
        filename,
    )
