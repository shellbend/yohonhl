"""Test cases for the __main__ module."""

from typing import Any

import pytest
from click.testing import CliRunner

from yohonhl import __main__
from yohonhl import api


@pytest.fixture()
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_goals_succeeds(
    runner: CliRunner, linescore_data: Any, requests_mock: Any
) -> None:
    """Goals subcommand succeeds."""
    resp_data, expected_goals = linescore_data
    requests_mock.get(f"{api.URL}/score/now", json=resp_data)
    result = runner.invoke(__main__.main, ["goals"])
    assert result.exit_code == 0
    assert result.output
