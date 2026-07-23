from unittest.mock import patch

from typer.testing import CliRunner

from text2gherkin.adapters.cli import app

runner = CliRunner()

VALID_GHERKIN = "Feature: X\n\n  Scenario: Y\n    Given a\n    When b\n    Then c\n"


def test_convert_file_to_file(tmp_path):
    input_file = tmp_path / "input.txt"
    input_file.write_text("some input text", encoding="utf-8")
    output_file = tmp_path / "output.feature"

    with patch("text2gherkin.adapters.cli.convert", return_value=VALID_GHERKIN):
        result = runner.invoke(app, ["convert", str(input_file), "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.read_text(encoding="utf-8") == VALID_GHERKIN


def test_convert_stdin_to_stdout():
    with patch("text2gherkin.adapters.cli.convert", return_value=VALID_GHERKIN):
        result = runner.invoke(app, ["convert"], input="some input text")

    assert result.exit_code == 0
    assert result.output == VALID_GHERKIN


def test_convert_failure_exits_nonzero_with_stderr():
    with patch("text2gherkin.adapters.cli.convert", side_effect=ValueError("boom")):
        result = runner.invoke(app, ["convert"], input="some input text")

    assert result.exit_code == 1
    assert "boom" in result.output
