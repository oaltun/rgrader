from typer.testing import CliRunner

from rgrader.cli import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["item", "create", "book1"])
    assert result.exit_code == 0
    assert "Creating item: book1" in result.stdout
