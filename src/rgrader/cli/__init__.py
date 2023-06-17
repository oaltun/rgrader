import typer
from typer import Typer

from rgrader.cli import env, grade, hello,merge

app: Typer = typer.Typer()

app.add_typer(env.app, name="env")
app.add_typer(hello.app, name="hello")
app.add_typer(grade.app, name="grade")
app.add_typer(merge.app, name="merge")


def rgrader() -> None:
    app()


if __name__ == "__main__":
    app()
