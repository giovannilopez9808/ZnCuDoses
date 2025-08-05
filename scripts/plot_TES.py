from matplotlib.axes import Axes
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


def plot_TES(
    data: DataFrame,
    ax: Axes,
    hour: int,
    label: str,
    color: str,
) -> None:
    if hour == 11:
        data = data[
            data["Initial_hour"] == hour
        ]
    if hour <= 8:
        data = data[
            data["Initial_hour"] <= hour
        ]
    ax.plot(
        data["Date"],
        data["TES"]/60,
        label=label,
        color=color,
    )


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
    zn_data = _tes[
        _tes["Particule"] == "zn"
    ]
    cu_data = _tes[
        _tes["Particule"] == "cu"
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
    fig, ax1 = pyplot.subplots(
        figsize=(
            20,
            5,
        ),
        # ncols=2,
    )
    plot_TES(
        data=zn_data,
        ax=ax1,
        hour=11,
        label="Zn noon",
        color="red",
    )
    plot_TES(
        data=zn_data,
        ax=ax1,
        hour=8,
        label="Zn sunrise",
        color="green",
    )
    plot_TES(
        data=cu_data,
        ax=ax1,
        hour=11,
        label="Cu noon",
        color="blue",
    )
    plot_TES(
        data=cu_data,
        ax=ax1,
        hour=8,
        label="Cu sunrise",
        color="purple",
    )
    ax2 = ax1
    # ax2 = ax1.twinx()
    # ax1.set_ylabel(
    # "Irradiancia máxima diaria (W/m$^2$)",
    # fontsize=16,
    # )
    ax2.set_ylabel(
        "TES (hour)",
        # rotation=-90,
        fontsize=16,
        # labelpad=25,
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
