from datetime import timedelta, datetime
from pathlib import Path
from typing import Annotated, Dict, List, Literal, Optional
from rich import print
import pandas as pd
from pydantic import BaseModel
import inspect


import typer

from rgrader.settings import settings

app = typer.Typer()

tr2en = str.maketrans("çğıöşü ", "cgiosu_")
def fix_colname(input: str, pre:str="", ex:str="ogr_no")->str:
    try:
        new_name = input.lower().translate(tr2en)
        if new_name == ex:
            return new_name
        else:
            return pre + "." + new_name
    except:
        return input


@app.command()
def xlsx(
    file_names:List[str]=["vize","proje","final"],
    input_dir:Path=Path("."),
    output_dir:Path=Path("."), 
    merge_on:str="ogr_no",
    )->None:

    full_df:pd.DataFrame=None
    df_s:List[pd.DataFrame] = []
    for iteration, exam_name in enumerate(file_names):
        path = Path(input_dir, f"{exam_name}.xlsx")
        print(path)

        ## Read the excel 
        df = pd.read_excel(path)

        ## Fix col names
        new_names = {old_colname: fix_colname(old_colname,exam_name,merge_on) for old_colname in df.columns}
        df.rename(columns=new_names, inplace=True)
        print("columns:", df.columns)
        df.to_excel(Path(output_dir, f"cleaned.{exam_name}.xlsx"))

        print(df["ogr_no"].head())

        if iteration == 0:
            print("assigning")
            full_df=df
        else:
            print("merging")
            full_df = full_df.merge(df, on=merge_on, how="outer")

    full_df.to_excel(Path(output_dir, "merged.xlsx"))