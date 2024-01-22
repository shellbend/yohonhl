"""Unit tests for the yohonhl.api module."""

import json
from typing import Any

import pytest

from yohonhl import api


def test_get_team_schedule_for_season(requests_mock: Any) -> None:
    """Test ability to get team schedule for entire season."""
    team = "COL"
    resp = {
        "previousSeason": 20222023,
        "currentSeason": 20232024,
        "clubTimezone": "America/Denver",
    }
    requests_mock.get(
        f"{api.URL}/club-schedule-season/{team}/now", text=json.dumps(resp)
    )
    assert api.get_team_schedule(team) == resp


def test_get_team_schedule_for_date(requests_mock: Any) -> None:
    """Test getting team schedule for specific date."""
    team = "COL"
    datestr = api.DateStr.WEEK
    resp = {
        "previousSeason": 20222023,
        "currentSeason": 20232024,
        "clubTimezone": "America/Denver",
    }
    requests_mock.get(
        f"{api.URL}/club-schedule/{team}/{datestr.value}", text=json.dumps(resp)
    )
    assert api.get_team_schedule(team, datestr=datestr) == resp


def test_get_schedule_for_all_teams_now(requests_mock: Any) -> None:
    """Test getting the current schedule for all teams."""
    resp = {"foo": "bar"}
    requests_mock.get(f"{api.URL}/schedule/now", text=json.dumps(resp))
    assert api.get_schedule() == resp


def test_get_schedule_for_date(requests_mock: Any) -> None:
    """Test getting the schedule for all teams on a specific date."""
    resp = {"foo": "bar"}
    datestr = "2024-01-01"
    requests_mock.get(f"{api.URL}/schedule/{datestr}", text=json.dumps(resp))
    assert api.get_schedule(datestr) == resp


def test_get_schedule_with_bad_date_raises(requests_mock: Any) -> None:
    """Test that an incorrect date supplied ot get_schedule raises value error."""
    resp = {"foo": "bar"}
    datestr = "not-a-date"
    requests_mock.get(f"{api.URL}/schedule/{datestr}", text=json.dumps(resp))
    with pytest.raises(
        ValueError, match=f"time data {datestr!r} does not match format '%Y-%m-%d'"
    ):
        api.get_schedule(datestr=datestr)


def test_get_linescores(requests_mock: Any) -> None:
    """Test get_linescores."""
    resp = {"foo": "bar"}
    requests_mock.get(f"{api.URL}/score/now", text=json.dumps(resp))
    assert api.get_linescores() == resp


def test_get_boxscores(requests_mock: Any) -> None:
    """Test get_boxscores."""
    resp = {"foo": "bar"}
    game_id = 2024020202
    requests_mock.get(f"{api.URL}/gamecenter/{game_id}/boxscore", text=json.dumps(resp))
    assert api.get_boxscores(game_id) == resp
