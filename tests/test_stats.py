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
    mock_aioresponse.get(ep_match_schedule, payload=schedule_data)
    games = list(stats.get_games())
    assert len(games) == 29


def test_get_goals(
    linescore_data: tuple[dict[str, Any], list[stats.Goal]],
    mock_aioresponse: aioresponses,
    ep_match_schedule: re.Pattern[AnyStr],
    ep_match_game: re.Pattern[AnyStr],
) -> None:
    """Test getting goals."""
    resp_data, expected_goals = linescore_data
    schedule = {"gameWeek": [resp_data]}
    mock_aioresponse.get(ep_match_schedule, payload=schedule)
    mock_aioresponse.get(ep_match_game, payload=resp_data)
    goals = list(stats.get_goals(start_date="2024-01-01"))
    assert len(goals) == len(expected_goals)
    for g, eg in zip(goals, expected_goals):
        assert g == eg
