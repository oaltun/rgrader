from datetime import timedelta, datetime
from pathlib import Path
from typing import Annotated, Dict, List, Literal, Optional
from rich import print
import pandas as pd


import typer

from rgrader.settings import settings

app = typer.Typer()


@app.command()
def settings_print():
    print(
        settings.dict,
    )



tr2en = str.maketrans("çğıöşü ", "cgiosu_")
def fix_colname(name:str):
    return name.lower().translate(tr2en)



comma2dot = str.maketrans(",",".")
def to_float(s: str):
    try:
        s=s.translate(comma2dot)
        return float(s)
    except AttributeError as e:
        return s




@app.command()
def ytu_exam_details_report():
    ## Student points from this exam is calculated using the formula 
    # round(max(min(120(p/e)-20(t-a)/(z-a), 100),0))
    # where 
    # e is the maximum possible raw points one can get from the exam, 
    # p is the students raw points, 
    # a is the start time of the exam, 
    # z is the end time of the exam, and
    # t is the time student finishes the exam. 
    e: float = settings.max_possible_raw_points
    a: datetime = settings.exam_start_time
    z: datetime = settings.exam_end_time

    ## Read by default 1st sheet of the excel file
    df = pd.read_excel(settings.excel_file_path)
    shape1=df.shape

    ## Get rid of Turkish only characters and blank in column names
    new_names = {col:fix_colname(col) for col in df.columns}
    df.rename(columns=new_names,inplace=True)

    ## Get rid of bad questions
    df = df[~df["id"].isin(settings.bad_questions)]

    ## Convert NaNs to 0
    df = df.fillna(0)

    ## Parse alinan_puan as float
    df.alinan_puan = df.alinan_puan.apply(to_float)


    ## Find each student, and calculate their points
    ogr_nos = df["ogrenci_numarasi"].unique()
    ps:List[float]=[]
    ts:List[datetime]=[]
    fps:List[float]=[]
    for index, ogr_no in enumerate(ogr_nos):
        answers = df[df["ogrenci_numarasi"]==ogr_no]
        p=float(sum(answers.alinan_puan))
        ps.append(p)
        if p>0:
            tstr = max(answers.cevap_tarihi)
            # Parse the time string, which will look like "13.06.2023 19:02:26"
            t = datetime.strptime(tstr,'%d.%m.%Y %H:%M:%S')
            final_point = round(max(min(120*(p/e)-20*((t-a)/(z-a)), 100),0))
            ts.append(t)
            fps.append(final_point)
        else:
            ts.append(z)
            fps.append(0)

    ## convert data to excell
    rdf1 = pd.DataFrame(dict(ham_puan= ps,sinav_bitiris=ts,ogr_no=ogr_nos,son_not= fps))
    rdf1.to_excel(Path(settings.excel_out_dir,"notlar_tum.xlsx"))   





