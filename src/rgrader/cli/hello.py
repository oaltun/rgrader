import typer
from dotenv import dotenv_values

from rgrader.settings import settings

app = typer.Typer()


@app.command()
def greet(name: str):
    print(f"Hello {name}")
