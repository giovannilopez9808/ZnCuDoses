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
        lw=5,
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
        tick.replace(
            month=tick.day,
            day=1,
        )
        for tick in ticks
    )
    ticks = list(
        tick.strftime(
            "%b"
        )
        for tick in ticks
    )
    fig, ax1 = pyplot.subplots(
        figsize=(
            8,
            5,
        ),
        # ncols=2,
    )
    ax2 = ax1.twinx()
    plot_TES(
        data=zn_data,
        ax=ax1,
        hour=11,
        label="Zn noon",
        color="black",
    )
    plot_TES(
        data=zn_data,
        ax=ax1,
        hour=8,
        label="Zn sunrise",
        color="grey",
    )
    plot_TES(
        data=cu_data,
        ax=ax1,
        hour=11,
        label="Cu noon",
        color="red",
    )
    plot_TES(
        data=cu_data,
        ax=ax1,
        hour=8,
        label="Cu sunrise",
        color="brown",
    )
    ax1.set_ylabel(
        "HT CuFe$_2$O$_4$ (hours)",
        fontsize=16,
    )
    ax2.set_ylabel(
        "HT ZnFe$_2$O$_4$ (hours)",
        rotation=-90,
        fontsize=16,
        labelpad=25,
    )
    ax1.set_xlim(
        dates[0],
        dates[-1],
    )
    ax1.set_ylim(
        0,
        12,
    )
    ax2.set_ylim(
        0,
        6,
    )
    ax1.set_xticks(
        dates,
    )
    ax1.set_xticklabels(
        ticks,
    )
    ax1.tick_params(
        labelsize=16,
        pad=8,
    )
    ax2.tick_params(
        labelsize=16,
        pad=8,
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
