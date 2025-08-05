from scipy.integrate import trapezoid
from os import system as terminal
from numpy import array, loadtxt
from os.path import join
from tqdm import tqdm
from pandas import (
    DataFrame,
    read_csv,
)


class TUV:
    def __init__(
        self,
    ) -> None:
        pass

    @staticmethod
    def _create_input_TUV_file(
        input_file: str,
        output_file: str,
        aod: float,
        ozone: float,
        year: int,
        month: int,
        day: int,
        hour: int,
        wavelenght_i: int,
        wavelenght_f: int,
    ) -> None:
        file = open(
            "./input_tuv.txt",
            "w"
        )
        text = " ".join([
            input_file,
            output_file,
            str(year),
            str(month),
            str(day),
            str(hour),
            str(aod),
            str(ozone),
            str(wavelenght_i),
            str(wavelenght_f),
        ])
        file.write(
            text,
        )
        file.close()

    def run(
        self,
        aod: float,
        ozone: float,
        year: int,
        month: int,
        day: int,
        hour: int,
        wavelength_i: int,
        wavelength_f: int,
        name: str,
        output: str,
        particule: str,
    ) -> DataFrame:
        self._create_input_TUV_file(
            name,
            output,
            aod,
            ozone,
            year,
            month,
            day,
            hour,
            wavelength_i,
            wavelength_f,
        )
        terminal(
            "./tuv"
        )
        results = self._read_TUV_output(
            "result.txt",
            wavelength_i,
            wavelength_f,
            particule,
            hour,
        )
        # terminal(
        # "rm ../results/*.txt"
        # )
        return results

    def _read_TUV_output(
        self,
        filename: str,
        wavelength_i: int,
        wavelength_f: int,
        particule: str,
        hour: int,
    ) -> float:
        rows = int(
            wavelength_f-wavelength_i
        )
        factors = self._read_factors(
            particule,
            wavelength_i,
            wavelength_f,
        )
        filename = join(
            "..",
            "results",
            filename,
        )
        data = loadtxt(
            filename,
            usecols=range(
                1,
                61,
            ),
            skiprows=5,
            max_rows=rows,
            dtype=str,
        )
        data = data.T
        data = DataFrame(
            data,
        )
        data = data.astype(
            float,
        )
        data = data.multiply(
            factors,
            axis=1,
        )
        data = data.apply(
            lambda values:
            trapezoid(
                values,
            ),
            axis=1,
        )
        data = DataFrame(
            data,
        )
        data.columns = [
            "Radiation",
        ]
        data.index.name = "Hours"

        data = data.reset_index()
        data["Hours"] = data["Hours"].apply(
            lambda minute:
            self._get_decimal_hour(
                hour,
                minute,
            )
        )
        return data

    @staticmethod
    def _get_decimal_hour(
        hour: int,
        minute: int,
    ) -> float:
        hour = hour+minute/60
        return hour

    @staticmethod
    def _read_factors(
        particule: str,
        wavelength_i: float,
        wavelength_f: float,
    ) -> array:
        filename = join(
            "..",
            "data",
            "absortion_factor_Cu_Zn.csv",
        )
        factors = read_csv(
            filename,
            index_col=0,
        )
        factors = factors[
            (
                factors.index >= wavelength_i+0.5
            ) &
            (
                factors.index <= wavelength_f-0.5
            )
        ]
        factors = factors[[
            particule
        ]]
        factors = factors.to_numpy()
        factors = factors.flatten()
        return factors


class TUVSearchAOD:
    def __init__(
        self,
    ) -> None:
        self.params = dict(
            AOD_initial=0.001,
            AOD_limite=5,
            RD_limite=10,
            RD_delta=1,
        )

    @staticmethod
    def _create_input_TUV_file(
        input_file: str,
        output_file: str,
        aod: float,
        ozone: float,
        year: int,
        month: int,
        day: int,
        hour: int,
    ) -> None:
        file = open(
            "./input_tuv.txt",
            "w"
        )
        text = " ".join([
            input_file,
            output_file,
            str(aod),
            str(ozone),
            str(year),
            str(month),
            str(day),
            str(hour),
        ])
        file.write(
            text,
        )
        file.close()

    def run(
        self,
        data: DataFrame,
    ) -> DataFrame:
        bar = tqdm(
            data.index,
        )
        results = DataFrame(
            columns=[
                "UVA+UVB",
                "AOD",
                "RD",
            ]
        )
        for index in bar:
            self._initialize_aod(
                self.params["AOD_initial"],
                self.params["AOD_limite"],
            )
            stop = False
            aod = self._get_new_aod(
                self.aod_i,
                self.aod_lim,
            )
            iter = 0
            while not (stop) and iter < 10:
                self._create_input_TUV_file(
                    "ROS",
                    "result",
                    aod,
                    data["Ozone"][index],
                    data["year"][index],
                    data["month"][index],
                    data["day"][index],
                    data["hour"][index],
                )
                terminal(
                    "./tuv"
                )
                data_model = self._read_TUV_output(
                    "result.txt",
                    data["minute"][index],
                )
                measurement = data["UVA+UVB"][index]
                stop, RD = self._get_RD_decision(
                    data_model,
                    measurement,
                )
                bar.set_postfix(
                    AOD=aod,
                    RD=RD,
                )
                if not stop:
                    aod = self._aod_binary_search(
                        aod,
                        RD,
                    )
                    rd_diff = abs(RD-self.params["RD_limite"])
                    is_upper_than_limit = self.aod_lim >= aod
                    is_lower_than_delta = rd_diff < self.params["RD_delta"]
                    if is_upper_than_limit and is_lower_than_delta:
                        stop = True
                    iter += 1
            results.loc[index] = [
                data_model,
                aod,
                RD,
            ]
        terminal(
            "rm ../results/*.txt"
        )
        return results

    def _initialize_aod(
        self,
        aod_i: float,
        aod_lim: float,
    ) -> None:
        """
        Funcion que inicializa el limite inferior y superior del AOD
        """
        self.aod_i = aod_i
        self.aod_lim = aod_lim

    def _get_new_aod(
        self,
        aod_i: float,
        aod_f: float,
    ) -> float:
        return round((aod_i+aod_f)/2, 3)

    def _get_RD_decision(
        self,
        model: float,
        measurement: float,
    ) -> tuple:
        """
        Funcion que calcula la RD entre el modelo y la medicion
        """
        stop = False
        RD = round(100*(model-measurement)/measurement, 3)
        if self._is_the_right_RD(RD):
            stop = True
        return stop, RD

    def _aod_binary_search(
        self,
        aod: float,
        RD: float,
    ) -> float:
        """
        Función que calcula el AOD que se introducira en el modelo SMARTS
        este emplea una busqueda binaria para que sea más eficiente
        """
        if self._is_the_right_RD(RD):
            self.aod_i = aod
        elif RD > self.params["RD_limite"]+self.params["RD_delta"]:
            self.aod_i = aod
        else:
            self.aod_lim = aod
        aod = self._get_new_aod(
            self.aod_lim,
            self.aod_i,
        )
        return aod

    def _is_the_right_RD(
        self,
        RD: float,
    ) -> bool:
        lim_i = self.params["RD_limite"]-self.params["RD_delta"]
        lim_f = self.params["RD_limite"]+self.params["RD_delta"]
        return lim_i < RD < lim_f

    @staticmethod
    def _read_TUV_output(
        filename: str,
        minute: int,
    ) -> float:
        filename = join(
            "..",
            "results",
            filename,
        )
        data = loadtxt(
            filename,
            usecols=range(
                2,
                62
            ),
            skiprows=3,
            max_rows=3,
        )
        data = DataFrame(
            data,
        )
        data = data.T
        data = data[[0, 2]]
        return data
