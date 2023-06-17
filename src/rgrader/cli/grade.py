from datetime import timedelta, datetime
from pathlib import Path
from typing import Annotated, Dict, List, Literal, Optional
from rich import print
import pandas as pd # type: ignore
from pydantic import BaseModel
import inspect


import typer

from rgrader.settings import settings

app = typer.Typer()


@app.command()
def settings_print()->None:
    print(
        settings.dict,
    )


tr2en = str.maketrans("çğıöşü ", "cgiosu_")


def fix_colname(name: str)->str:
    return name.lower().translate(tr2en)


comma2dot = str.maketrans(",", ".")


def to_float(s: str)->float|str:
    try:
        s = s.translate(comma2dot)
        return float(s)
    except AttributeError as e:
        return s


def to_datetime_nosec(tstr: str)->datetime|str:
    try:
        dt = datetime.strptime(tstr, '%d.%m.%Y %H:%M')
        return dt
    except:
        return tstr


def to_datetime(tstr: str)->datetime|str:
    try:
        dt = datetime.strptime(tstr, '%d.%m.%Y %H:%M:%S')
        return dt
    except:
        return tstr


def ytuexcel_2_dataframe(path: Path,bad_questions:List[int])->pd.DataFrame:
    ## Read by default 1st sheet of the excel file
    df = pd.read_excel(path)

    ## Get rid of Turkish only characters and blank in column names
    new_names = {col: fix_colname(col) for col in df.columns}
    df.rename(columns=new_names, inplace=True)

    ## Get rid of bad questions
    df = df[~df["id"].isin(bad_questions)]

    ## Parse *_puan as float
    df.alinan_puan = df.alinan_puan.apply(to_float)
    df.soru_puani = df.soru_puani.apply(to_float)

    ## Parse *_tarihi as datetime fields
    df.baslama_tarihi = df.baslama_tarihi.apply(to_datetime_nosec)
    df.bitirme_tarihi = df.bitirme_tarihi.apply(to_datetime_nosec)
    df.gorme_tarihi = df.gorme_tarihi.apply(to_datetime)
    df.cevap_tarihi = df.cevap_tarihi.apply(to_datetime)
    return df


class GraderYTU(BaseModel):
    puan_factor: float = 1.20
    zaman_factor: float = 0.20
    puan_ham_mumkun: float = 100
    zaman_sinav_baslama: datetime
    zaman_sinav_bitme: datetime 

    def grade(self, zaman_ogr_bitirme: datetime, puan_ham_ogr: float)-> int:
        puan_per100 = 100 * (puan_ham_ogr / self.puan_ham_mumkun)

        sure_sinav = self.zaman_sinav_bitme - self.zaman_sinav_baslama
        sure_ogr = zaman_ogr_bitirme - self.zaman_sinav_baslama
        zaman_per100 = 100 * (sure_ogr / sure_sinav)

        puan_son = self.puan_factor * puan_per100 - self.zaman_factor * zaman_per100
        puan_son = min(puan_son, 100)
        puan_son = max(puan_son, 0)
        puan_son = round(puan_son)
        return puan_son


@app.command()
def ytu_exam_details_report(
    excel_file_path: Path = Path(
        "/mnt/c/Users/oguz/OneDrive/donem-2022-2/hesaplama_kurami/final_excel/BLM2502 - 1_Final_Detay_Raporu_14-06-23-13-22.xlsx"
    ),
    excel_out_dir: Path = Path("/mnt/c/Users/oguz/OneDrive/donem-2022-2/hesaplama_kurami/final_excel"),
    bad_questions: List[int] = [1000001,10000000002],
    puan_ham_mumkun: float = float(270),
    zaman_sinav_baslama: datetime = datetime(year=2023, month=6, day=5, hour=19),
    zaman_sinav_bitme: datetime = datetime(year=2023, month=6, day=5, hour=19, minute=40),
    puan_factor: float = 1.20,
    zaman_factor: float = 0.20
)->None:
    grader = GraderYTU(  
        puan_factor=puan_factor,
        zaman_factor=zaman_factor,
        puan_ham_mumkun=puan_ham_mumkun,
        zaman_sinav_baslama=zaman_sinav_baslama,
        zaman_sinav_bitme=zaman_sinav_bitme
    )

    df = ytuexcel_2_dataframe(excel_file_path,bad_questions)

    df.to_excel(Path(excel_out_dir, "cleaned_tum.xlsx"))

    ## Select each student and calculate their points
    ogr_nos = df["ogrenci_numarasi"].unique()
    ps: List[float] = []
    ts: List[datetime] = []
    fps: List[float] = []
    emails: List[str] = []
    ads: List[str] = []
    soyads: List[str] = []
    for index, ogr_no in enumerate(ogr_nos):
        answers = df[df["ogrenci_numarasi"] == ogr_no]

        puan_ham_ogr = float(answers.alinan_puan.sum())
        ps.append(puan_ham_ogr)

        email = answers.eposta.unique()
        assert len(email) == 1
        emails.append(email[0])

        ad = answers.ad.unique()
        assert len(ad) == 1
        ads.append(ad[0])

        soyad = answers.soyad.unique()
        assert len(soyad) == 1
        soyads.append(soyad[0])

        if puan_ham_ogr > 0:
            zaman_ogr_bitirme = answers.cevap_tarihi.max()
            final_point = grader.grade(zaman_ogr_bitirme, puan_ham_ogr)
            ts.append(zaman_ogr_bitirme)
            fps.append(final_point)
        else:
            ts.append(grader.zaman_sinav_bitme)
            fps.append(0)

    ## Write data to excell
    mindatadf = pd.DataFrame(dict(puan_ham=ps, zaman_ogr_bitirme=ts, ogr_no=ogr_nos, puan_son=fps))
    datadf = pd.DataFrame(
        dict(puan_ham=ps, zaman_ogr_bitirme=ts, eposta=emails, ad=ads, soyad=soyads, ogr_no=ogr_nos, puan_son=fps)
    )
    infodf = pd.DataFrame(
        columns=[
            "self.puan_factor",
            "self.zaman_factor",
            "self.puan_ham_mumkun",
            "self.zaman_sinav_baslama",
            "self.zaman_sinav_bitme",
            "son_not hesaplama metodu",
        ],
        data=[
            [
                grader.puan_factor,
                grader.zaman_factor,
                grader.puan_ham_mumkun,
                grader.zaman_sinav_baslama,
                grader.zaman_sinav_bitme,
                inspect.getsource(grader.grade),
            ]
        ],
    )

    with pd.ExcelWriter(Path(excel_out_dir, "notlar_tum.xlsx")) as writer:
        datadf.to_excel(writer, sheet_name="data")
        infodf.to_excel(writer, sheet_name="info")

    with pd.ExcelWriter(Path(excel_out_dir, "notlar_onlyno.xlsx")) as writer:
        mindatadf.to_excel(writer, sheet_name="data")
        infodf.to_excel(writer, sheet_name="info")
