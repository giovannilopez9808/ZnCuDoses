from scipy.integrate import trapezoid
from itertools import product
from modules.TUV import TUV
from os.path import join
from pandas import (
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
    params["data"],
    params["dates"],
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
    for particule_name, month in data:
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
        radiation["Hours"] = radiation["Hours"]*3600
        tes, tuv_dose = find_TES(
            radiation,
            particule["doses"],
        )
        ratio = tuv_dose/particule["doses"]
        results.loc[len(results)] = [
            city["Ciudad"],
            date.strftime("%Y-%m-%d"),
            particule_name,
            tes,
            tuv_dose,
            ratio,
        ]
        print(results)
results.to_csv(
    "ZnCuDoses.csv",
    index=False,
)
