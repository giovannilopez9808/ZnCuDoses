from itertools import product
from modules.TUV import TUV
from os.path import join
from os import makedirs
from pandas import (
    to_datetime,
    Timestamp,
    DataFrame,
    read_csv,
    Series,
    concat,
)


def get_hhmm_from_hour_decimal(
    hour: float,
) -> str:
    minute = round(
        hour % 1*60
    )
    hour = int(
        hour
    )
    hour = f"{hour}:{minute}"
    return hour


def get_datetime(
    date: Timestamp,
    hours: Series,
) -> Series:
    datetime = hours.apply(
        lambda hour:
        to_datetime(
            f"{date.date()} {hour}"
        )
    )
    return datetime


params = dict(
    dates=range(
        1,
        13,
    ),
    data=dict(
        zn=dict(
            wavelength=631.5,
            factor=0.32711,
            doses=4264,
        ),
        cu=dict(
            wavelength=745.5,
            factor=0.4645,
            doses=13,
        ),
    )
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
    params["dates"],
    params["data"],
)
data = list(data)
model = TUV()
results = DataFrame(
    columns=[
        "City",
        "Date",
        "Particule",
        "TES",
        "TUV Dose",
        "Dose ratio",
    ]
)
for name in dataset.index:
    city = dataset.loc[name]
    city_dataset = {
        particule_name: DataFrame()
        for particule_name in params["data"]
    }
    for month, particule_name in data:
        date = to_datetime(
            f"2024-{month}-21"
        )
        particule = params["data"][particule_name]
        radiation = DataFrame()
        for hour in range(12, 20):
            inputs = dict(
                wavelength=particule["wavelength"],
                aod=city["AOD550nm"],
                ozone=250,
                # ozone=city["Ozone"],
                month=date.month,
                year=date.year,
                day=date.day,
                hour=hour,
                name=name,
                output="results",
            )
            _radiation = model.run(
                **inputs,
            )
            radiation = concat([
                radiation,
                _radiation,
            ])
        radiation["Radiation"] = radiation["Radiation"] * particule["factor"]
        radiation = radiation.rename(
            columns={
                "Radiation": particule_name
            },
        )
        radiation["Hours"] = radiation["Hours"].apply(
            get_hhmm_from_hour_decimal
        )
        radiation.index = get_datetime(
            date,
            radiation["Hours"],
        )
        radiation = radiation.drop(
            columns=[
                "Hours",
            ]
        )
        city_dataset[particule_name] = concat([
            city_dataset[particule_name],
            radiation,
        ])
    results = concat(
        city_dataset.values(),
        axis=1,
    )
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
    results.to_csv(
        filename,
    )
