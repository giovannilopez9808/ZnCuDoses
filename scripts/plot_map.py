from matplotlib.gridspec import GridSpec
from matplotlib.pyplot import figure
from matplotlib.image import imread
from matplotlib.lines import Line2D
from matplotlib.axes import Axes
from pandas import read_csv
from os.path import join
from sys import argv


def plot_image(
    filename: str,
    ax: Axes,
) -> None:
    image = imread(
        filename,
    )
    ax.imshow(
        image,
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis(
        "off",
    )


def plot_location(
    ax: Axes,
    longitude: float,
    latitude: float,
) -> None:
    longitude = longitude+180
    longitude = longitude/360
    longitude = longitude*720
    latitude = latitude*-1
    latitude = latitude+90
    latitude = latitude/180
    latitude = latitude*360
    ax.scatter(
        longitude,
        latitude,
        color="black",
        s=500,
    )


def plot_text(
    ax: Axes,
    text: str,
    x: float,
    y: float,
) -> None:
    text = ax.text(
        x,
        y,
        text,
        horizontalalignment='center',
        weight="bold",
        fontdict={
            "size": 40,
        },
    )
    # text.set_path_effects(
    # [
    # patheffects.withStroke(
    # linewidth=5,
    # foreground='w',)
    # ]
    # )


fig = figure(
    figsize=(
        80,
        50,
    )
)
grid = GridSpec(
    nrows=4,
    ncols=6,
    wspace=0,
    hspace=0,
)
filename = join(
    "..",
    "data",
    "data.csv"
)
dataset = read_csv(
    filename,
    index_col=0,
)
dataset = dataset[[
    "Latitud",
    "Longitud",
]]
dataset = dataset.astype(
    float,
)
up_1 = fig.add_subplot(
    grid[0, 1],
)
up_2 = fig.add_subplot(
    grid[0, 2],
)
up_3 = fig.add_subplot(
    grid[0, 3],
)
up_4 = fig.add_subplot(
    grid[0, 4],
)
world = fig.add_subplot(
    grid[1:3, 1:5],
)
right_1 = fig.add_subplot(
    grid[1, 5]
)
right_2 = fig.add_subplot(
    grid[2, 5]
)
left_1 = fig.add_subplot(
    grid[1, 0],
)
left_2 = fig.add_subplot(
    grid[2, 0],
)
down_1 = fig.add_subplot(
    grid[3, 1],
)
down_2 = fig.add_subplot(
    grid[3, 2],
)
down_3 = fig.add_subplot(
    grid[3, 3],
)
down_4 = fig.add_subplot(
    grid[3, 4],
)
filename = join(
    "..",
    "graphics",
    "map.png",
)
plot_image(
    filename,
    world,
)
axs = dict(
    LA=up_1,
    NY=up_2,
    LON=up_3,
    ZUR=up_4,
    MED=down_1,
    CAR=down_2,
    SAN=down_3,
    ROS=down_4,
    MTY=left_1,
    CDMX=left_2,
    MUM=right_1,
    SHA=right_2,
)
for city, ax in axs.items():
    city_dataset = dataset.loc[city]
    filename = f"{city}.png"
    filename = join(
        "..",
        "graphics",
        f"TES_{argv[1]}",
        filename,
    )
    plot_image(
        filename,
        ax,
    )
    plot_location(
        world,
        city_dataset["Longitud"],
        city_dataset["Latitud"],
    )
plot_text(
    world,
    "Los Angeles",
    100+20,
    105,
)
plot_text(
    world,
    "New York",
    190+20,
    110,
)
plot_text(
    world,
    "London",
    350+20,
    70,
)
plot_text(
    world,
    "Zurich",
    380+20,
    85,
)
plot_text(
    world,
    "Shanghai",
    570+20,
    130,
)
plot_text(
    world,
    "Mumbai",
    490+20,
    135,
)
plot_text(
    world,
    "Monterrey",
    135+20,
    120,
)
plot_text(
    world,
    "Mexico City",
    140+20,
    155,
)
plot_text(
    world,
    "Cartagena",
    205+20,
    150,
)
plot_text(
    world,
    "Medellin",
    200+20,
    180,
)
plot_text(
    world,
    "Rosario",
    220+20,
    240,
)
plot_text(
    world,
    "Santiago",
    190+20,
    265,
)
colors = dict()
if argv[1] != "Cu":
    colors.update(
        {
            "1": dict(
                name="HT-ZnFe$_2$O$_4$ noon",
                color="red",
            ),
            "2": dict(
                name="HT-ZnFe$_2$O$_4$ sunrise",
                color="orange",
            )
        }
    )
if argv[1] != "Fe":
    colors.update(
        {
            "3": dict(
                name="HT-CuFe$_2$O$_4$ noon",
                color="blue",
            ),
            "4": dict(
                name="HT-CuFe$_2$O$_4$ sunrise",
                color="#00b4d8",
            ),
        }
    )
custom_lines = list(
    Line2D(
        [0],
        [0],
        color=data["color"],
        lw=30,
    )
    for data in colors.values()
)
labels = list(
    data["name"]
    for data in colors.values()
)
world.legend(
    custom_lines,
    labels,
    frameon=False,
    loc="lower center",
    bbox_to_anchor=(
        0.5,
        -0.1,
    ),
    fontsize=60,
    ncols=4,
)
fig.tight_layout(
    h_pad=0,
    w_pad=0,
    pad=0,
)
folder = join(
    "..",
    "graphics",
    f"TES_{argv[1]}.pdf"
)
fig.savefig(
    folder,
)
