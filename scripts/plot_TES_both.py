from matplotlib.axes import Axes
from matplotlib import pyplot
from numpy import linspace
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
    particule: str,
) -> None:
    if hour == 11:
        data = data[
            data["Initial_hour"] == hour
        ]
    if hour <= 8:
        data = data[
            data["Initial_hour"] <= hour
        ]
    if particule == "Cu":
        data.loc[:, "TES"] = data["TES"]
    if particule == "Zn":
        data.loc[:, "TES"] = data["TES"]/60
    ax.plot(
        data["Date"],
        data["TES"],
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
    TES_limit = dataset.loc[name, "TES_limit"]
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
            "%m"
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
        particule="Zn",
        color="red",
    )
    plot_TES(
        data=zn_data,
        ax=ax1,
        hour=8,
        label="Zn sunrise",
        particule="Zn",
        color="orange",
    )
    plot_TES(
        data=cu_data,
        ax=ax2,
        hour=11,
        label="Cu noon",
        particule="Cu",
        color="blue",
    )
    plot_TES(
        data=cu_data,
        ax=ax2,
        hour=8,
        label="Cu sunrise",
        particule="Cu",
        color="#00b4d8",
    )
    # ax2.yaxis.label.set_color('red')
    # ax1.yaxis.label.set_color('black')
    # ax2.tick_params(
    # colors="red",
    # axis="y",
    # )
    # ax1.tick_params(
    # colors="black",
    # axis="y",
    # )
    ax2.set_title(
        city_name,
        weight="bold",
        fontsize=26,
    )
    ax2.set_ylabel(
        "HT-CuFe$_2$O$_4$ (min)",
        weight="bold",
        color="blue",
        fontsize=20,
        rotation=-90,
        labelpad=25,
    )
    ax1.set_ylabel(
        "HT-ZnFe$_2$O$_4$ (h)",
        weight="bold",
        fontsize=20,
        color="red",
    )
    ax2.set_xlim(
        dates[0],
        dates[-1],
    )
    ax2.set_ylim(
        0,
        TES_limit,
    )
    ax2.set_yticks(
        linspace(
            0,
            TES_limit,
            7,
        ),
    )
    ax1.set_ylim(
        0,
        12,
    )
    ax1.set_yticks(
        range(
            0,
            14,
            2,
        )
    )
    ax2.set_xticks(
        dates,
    )
    ax2.set_xticklabels(
        ticks,
    )
    ax2.set_xlabel(
        "Month",
        weight="bold",
        fontsize=24,
    )
    ax2.tick_params(
        labelsize=20,
        width=2,
        size=5,
        pad=8,
    )
    ax1.tick_params(
        labelsize=20,
        width=2,
        size=5,
        pad=8,
    )
    ax2.axhline(
        y=120,
        color="black",
        ls="--",
        lw=3,
    )
    folder = join(
        "..",
        "graphics",
        "TES_both"
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
