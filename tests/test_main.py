"""Test cases for the __main__ module."""

import re
from typing import Any

import pytest
from aioresponses import aioresponses
from click.testing import CliRunner

from yohonhl import __main__


@pytest.fixture()
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_goals_succeeds(
    runner: CliRunner,
    ep_match_schedule: re.Pattern[str],
    ep_match_game: re.Pattern[str],
    schedule_data: dict[str, Any],
    game_data: dict[str, Any],
    mock_aioresponse: aioresponses,
) -> None:
    """Goals subcommand succeeds."""
    mock_aioresponse.get(ep_match_schedule, payload=schedule_data, repeat=True)
    mock_aioresponse.get(ep_match_game, payload=game_data, repeat=True)
    result = runner.invoke(__main__.main, ["-v", "goals"])
    assert result.exit_code == 0
    assert result.output
