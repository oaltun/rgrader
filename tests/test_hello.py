from typer.testing import CliRunner

from rgrader.cli import app

runner = CliRunner()


# def test_app():
#     result = runner.invoke(app, ["item", "create", "book1"])
#     assert result.exit_code == 0
#     assert "Creating item: book1" in result.stdout


def test_greet():
    result = runner.invoke(app, ["hello", "greet", "Oguz"])
    assert result.exit_code == 0
    assert "Hello Oguz" in result.stdout
