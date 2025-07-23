from matplotlib import pyplot
from os.path import join
from typing import List
from pandas import (
    DataFrame,
    Timestamp,
    read_csv,
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
    dates = get_dates(
        radiation,
    )
    pyplot.subplots(
        figsize=(
            18,
            10,
        )
    )
    pyplot.plot(
        radiation,
    )
    pyplot.xticks(
        dates,
    )
    pyplot.show()
    exit(1)
