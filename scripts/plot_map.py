from matplotlib.gridspec import GridSpec
from matplotlib.pyplot import figure
from matplotlib.image import imread
from matplotlib.lines import Line2D
from matplotlib import patheffects
from matplotlib.axes import Axes
from os.path import join


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
        fontdict={
            "size": 30,
        },
    )
    text.set_path_effects(
        [
            patheffects.withStroke(
                linewidth=5,
                foreground='w',)
        ]
    )


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


legend = fig.add_subplot(
    grid[0, 0],
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
    filename = f"{city}.png"
    filename = join(
        "..",
        "graphics",
        "TUV",
        filename,
    )
    plot_image(
        filename,
        ax,
    )
plot_text(
    world,
    "Los Angeles",
    100+20,
    110,
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
    80,
)
plot_text(
    world,
    "Zurich",
    370+20,
    85,
)
plot_text(
    world,
    "Shangai",
    570+20,
    125,
)
plot_text(
    world,
    "Mumbai",
    490+20,
    140,
)
plot_text(
    world,
    "Monterrey",
    135+20,
    120,
)
plot_text(
    world,
    "Ciudad\nde México",
    140+20,
    140,
)
plot_text(
    world,
    "Cartagena",
    340+20,
    105,
)
plot_text(
    world,
    "Medellin",
    200+20,
    175,
)
plot_text(
    world,
    "Rosario",
    220+20,
    245,
)
plot_text(
    world,
    "Santiago\nde\nChile",
    200+20,
    245,
)
colors = {
    "1": dict(
        name="HT ZnFe$_2$O$_4$ mediodia",
        color="black",
    ),
    "2": dict(
        name="HT ZnFe$_2$O$_4$ amanecer",
        color="grey",
    ),
    "3": dict(
        name="HT CuFe$_2$O$_4$ mediodia",
        color="red",
    ),
    "4": dict(
        name="HT CuFe$_2$O$_4$ amanecer",
        color="brown",
    ),
}

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
legend.axis(
    "off"
)
legend.legend(
    custom_lines,
    labels,
    loc="center",
    fontsize=60,
)
fig.tight_layout(
    h_pad=0,
    w_pad=0,
    pad=0,
)
fig.savefig(
    "test.pdf"
)
