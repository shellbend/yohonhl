"""Unit tests for yohonhl.stats module."""

import re
from typing import Any
from typing import AnyStr

from aioresponses import aioresponses

from yohonhl import stats


def test_get_games(
    schedule_data: list[dict[str, Any]],
    mock_aioresponse: aioresponses,
    ep_match_schedule: re.Pattern[str],
) -> None:
    """Get games from schedule."""
    mock_aioresponse.get(ep_match_schedule, payload=schedule_data, repeat=True)
    games = list(stats.get_games())
    assert len(games) == 35


def test_get_games_with_bad_dates(
    schedule_data: list[dict[str, Any]],
    mock_aioresponse: aioresponses,
    ep_match_schedule: re.Pattern[str],
) -> None:
    """Get games from schedule with to date before from."""
    mock_aioresponse.get(ep_match_schedule, payload=schedule_data, repeat=True)
    games = list(stats.get_games(start_date="2024-02-01", end_date="2024-01-01"))
    assert len(games) == 35


def test_get_goals(
    game_data: dict[str, Any],
    game_data_without_scoring: dict[str, Any],
    schedule_data: dict[str, Any],
    mock_aioresponse: aioresponses,
    ep_match_schedule: re.Pattern[AnyStr],
    ep_match_game: re.Pattern[AnyStr],
) -> None:
    """Test getting goals."""
    mock_aioresponse.get(ep_match_schedule, payload=schedule_data, repeat=True)
    mock_aioresponse.get(ep_match_game, payload=game_data_without_scoring)
    mock_aioresponse.get(ep_match_game, payload=game_data, repeat=True)
    goals = list(stats.get_goals(start_date="2024-01-01"))
    assert len(goals) > 0
