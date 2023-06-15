import typer
from typer import Typer

from rgrader.cli import env, grade

app: Typer = typer.Typer()

app.add_typer(env.app, name="env")
app.add_typer(grade.app, name="grade")


def rgrader() -> None:
    app()


if __name__ == "__main__":
    app()
