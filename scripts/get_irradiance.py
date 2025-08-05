from itertools import product
from modules.TUV import TUV
from os.path import join
from tqdm import tqdm
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
            wavelength_i=419.5,
            wavelength_f=632.5,
            doses=1353600,
        ),
        cu=dict(
            wavelength_i=419.5,
            wavelength_f=746.5,
            doses=331200,
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
for name in tqdm(
    dataset.index,
    leave=False,
):
    city = dataset.loc[name]
    city_dataset = {
        particule_name: DataFrame()
        for particule_name in params["data"]
    }
    for month, particule_name in tqdm(
        data,
        leave=False,
    ):
        date = to_datetime(
            f"2024-{month}-21"
        )
        particule = params["data"][particule_name]
        radiation = DataFrame()
        for hour in range(5, 21):
            inputs = dict(
                wavelength_i=particule["wavelength_i"],
                wavelength_f=particule["wavelength_f"],
                particule=particule_name,
                aod=city["AOD550nm"],
                # ozone=city["Ozone"],
                month=date.month,
                output="results",
                year=date.year,
                day=date.day,
                hour=hour,
                ozone=250,
                name=name,
            )
            _radiation = model.run(
                **inputs,
            )
            radiation = concat([
                radiation,
                _radiation,
            ])
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
