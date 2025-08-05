from matplotlib import pyplot
from os.path import join
from typing import List
from pandas import (
    to_datetime,
    DataFrame,
    Timestamp,
    read_csv,
    merge,
)


def get_dates(
    data: DataFrame,
) -> List[Timestamp]:
    dates = sorted(
        set(
            data["Date"]
        )
    )
    return dates


def change_date(
    data: DataFrame,
) -> DataFrame:
    data["Date"] = data["Date"].apply(
        lambda date:
        date.replace(
            month=1,
            day=date.month
        )
    )
    return data


filename = join(
    "..",
    "data",
    "data.csv",
)
dataset = read_csv(
    filename,
    index_col="Nombre",
)
filename = join(
    "..",
    "results",
    "ZnCuDoses.csv",
)
tes = read_csv(
    filename,
)
tes["Date"] = to_datetime(
    tes["Date"],
)
tes = change_date(
    tes,
)
for name in dataset.index:
    city_name = dataset.loc[name, "Ciudad"]
    _tes = tes[
        tes["City"] == city_name
    ]
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
        "d"
    ).max()
    radiation = radiation.stack()
    radiation = radiation.reset_index()
    radiation = radiation.rename(
        columns={
            "level_0": "Date",
            "level_1": "Particule",
            0: "Radiation",
        },
    )
    data = merge(
        radiation,
        _tes,
        how="inner",
        on=[
            "Date",
            "Particule",
        ],
    )
    zn_data = data[
        (
            data["Particule"] == "zn"
        ) &
        (
            data["Initial_hour"] == 11
        )
    ]
    cu_data = data[
        (
            data["Particule"] == "cu"
        ) &
        (
            data["Initial_hour"] == 11
        )
    ]
    ticks = get_dates(
        zn_data,
    )
    dates = list(
        to_datetime(
            f"{tick}"
        )
        for tick in ticks
    )
    ticks = list(
        tick.strftime(
            "%Y-%d"
        )
        for tick in ticks
    )
    fig, (ax1, ax2) = pyplot.subplots(
        figsize=(
            40,
            5,
        ),
        ncols=2,
    )
    # ax2 = ax1.twinx()
    ax1.plot(
        zn_data["Date"],
        zn_data["Radiation"],
        color="red",
        label="Zn Irradiancia",
        marker="o"
    )
    ax2.plot(
        zn_data["Date"],
        zn_data["TES"],
        color="blue",
        label="Zn TES",
        marker="o"
    )
    ax1.plot(
        cu_data["Date"],
        cu_data["Radiation"],
        color="orange",
        label="Irradiancia Cu",
        marker="o"
    )
    ax2.plot(
        cu_data["Date"],
        cu_data["TES"],
        color="green",
        label="Cu TES",
        marker="o"
    )
    ax1.set_ylabel(
        "Irradiancia máxima diaria (W/m$^2$)",
        fontsize=16,
    )
    ax2.set_ylabel(
        "TES (min)",
        rotation=-90,
        fontsize=16,
        labelpad=25,
    )
    ax1.set_xticks(
        dates,
    )
    ax1.set_xticklabels(
        ticks,
    )
    ax1.tick_params(
        labelsize=16,
    )
    ax2.tick_params(
        labelsize=16,
    )
    fig.legend(
        bbox_to_anchor=(
            0.75,
            1.02,
        ),
        frameon=False,
        fontsize=16,
        ncols=4,
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
    fig.tight_layout(
        pad=3,
    )
    fig.savefig(
        filename,
    )
