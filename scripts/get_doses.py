from os import read
from scipy.integrate import trapezoid
from itertools import product
from modules.TUV import TUV
from os.path import join
from pandas import (
    Timestamp,
    to_datetime,
    DataFrame,
    read_csv,
    concat,
)


def find_TES(
    data: DataFrame,
    doses: float,
) -> int:
    total = len(data)
    found = False
    tes = 1
    while not found:
        _data = data.iloc[:tes]
        tuv_dose = trapezoid(
            _data["Radiation"],
            _data["Hours"]
        )
        if tuv_dose >= doses:
            return tes, tuv_dose
        else:
            tes += 1
        if tes == total:
            return None, tuv_dose


def get_decimal_hour_from_time(
    time: Timestamp,
) -> float:
    hour = time.hour
    minute = time.minute
    time = hour+minute/60
    return time


params = dict(
    dates=range(
        1,
        13,
    ),
    data=dict(
        zn=dict(
            doses=1353600,
        ),
        cu=dict(
            doses=331200,
        ),
    ),
    hours=[
        "sunrise",
        "noon",
    ],
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
data = product(
    params["data"],
    params["dates"],
    params["hours"],
)
data = list(
    data
)
results = DataFrame(
    columns=[
        "City",
        "Date",
        "Particule",
        "Initial_hour",
        "TES",
        "TUV Dose",
        "Dose ratio",
    ],
)
for name in dataset.index:
    city = dataset.loc[name]
    filename = f"{name}.csv"
    filename = join(
        "..",
        "results",
        "TUV",
        filename,
    )
    city_radiation = read_csv(
        filename,
        parse_dates=True,
        index_col=0,
    )
    for particule_name, month, hour in data:
        hour = city[hour]
        date = to_datetime(
            f"2024-{month}-21"
        )
        particule = params["data"][particule_name]
        radiation = city_radiation[[
            particule_name,
        ]]
        radiation = radiation[
            (
                radiation.index.date == date.date()
            ) &
            (
                radiation.index.hour >= hour
            )
        ]
        radiation["Hours"] = get_decimal_hour_from_time(
            radiation.index,
        )
        radiation["Hours"] = radiation["Hours"]*3600
        radiation = radiation.rename(
            columns={
                particule_name: "Radiation"
            },
        )
        tes, tuv_dose = find_TES(
            radiation,
            particule["doses"],
        )
        ratio = tuv_dose/particule["doses"]
        results.loc[len(results)] = [
            city["Ciudad"],
            date.strftime("%Y-%m-%d"),
            hour,
            particule_name,
            tes,
            tuv_dose,
            ratio,
        ]
results.to_csv(
    "ZnCuDoses.csv",
    index=False,
)
