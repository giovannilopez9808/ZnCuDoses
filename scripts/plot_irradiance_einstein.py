from matplotlib.pyplot import subplots
from matplotlib import pyplot
from numpy import linspace
from os.path import join
from typing import List
from pandas import (
    DataFrame,
    Timestamp,
    read_csv,
    to_datetime,
)
import matplotlib

pyplot.rc('text.latex', preamble=r'\usepackage{amsmath}')


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
planck = 6.623e-34
avogadro_number = 6.022e23
light_velocity = 3e8
constant = planck*avogadro_number*light_velocity
fig, axs = subplots(
    sharex=True,
    sharey=True,
    figsize=(
        24,
        10,
    ),
    ncols=4,
    nrows=3,
)
axs = axs.flatten()
for ax, name in zip(
    axs,
    dataset.index,
):
    city = dataset.loc[name]
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
    radiation = radiation.resample(
        "1d"
    ).max()
    radiation = radiation/constant
    ticks = get_dates(
        radiation,
    )
    dates = list(
        to_datetime(
            f"{tick}"
        )
        for tick in ticks
    )
    ticks = list(
        tick.strftime(
            "%d"
        )
        for tick in ticks
    )
    ax2 = ax.twinx()
    ax.plot(
        radiation["zn"],
        color="red",
    )
    ax2.plot(
        radiation["cu"],
        color="blue",
        lw=2,
    )
    ax.set_title(
        city["Ciudad"],
        weight="bold",
        fontsize=20,
    )
    ax.set_ylim(
        0,
        1200,
    )
    ax.set_yticks(
        linspace(
            0,
            1200,
            6,
        ),
    )
    ax2.set_ylim(
        0,
        3000,
    )
    ax2.set_yticks(
        linspace(
            0,
            3000,
            6,
        ),
    )
    if ax in axs[-4:]:
        ax.set_xlabel(
            "Month",
            weight="bold",
            fontsize=20,
        )
    if not ax in axs[3::4]:
        ax2.set_yticks([])
    ax.set_xlim(
        dates[0],
        dates[-1],
    )
    ax.set_xticks(
        dates,
        ticks,
    )
    ax.tick_params(
        labelsize=16,
    )
    ax2.tick_params(
        labelsize=16,
    )
fig.text(
    0.005,
    0.2,
    r"$\bf{E^{a}_{n,p}}$ HT-ZnFe$_2$O$_4$ (einstein/m$^2$s)",
    weight="bold",
    color="red",
    fontsize=22,
    rotation=90,
)
fig.text(
    0.98,
    0.2,
    r"$\bf{E^{a}_{n,p}}$ HT-CuFe$_2$O$_4$  (einstein/m$^2$s)",
    weight="bold",
    color="blue",
    rotation=-90,
    fontsize=22,
)
folder = join(
    "..",
    "graphics",
)
filename = "Radiation_einstein.png"
filename = join(
    folder,
    filename,
)
fig.tight_layout(
    pad=4,
)
fig.savefig(
    filename,
)
