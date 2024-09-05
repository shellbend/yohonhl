"""Unit tests for the yohonhl.api module."""

import re
from typing import Any
from typing import AnyStr

import pytest
from aioresponses import aioresponses

from yohonhl import api


def test_get_week_start_dates_with_more_than_one_week() -> None:
    """Get week starting dates with more than one week."""
    start, end, num_weeks, expected_start_dates = (
        "2024-01-01",
        "2024-02-01",
        5,
        ["2024-01-01", "2024-01-08", "2024-01-15", "2024-01-22", "2024-01-29"],
    )
    start_dates = api._get_week_start_dates(start, end)  # noqa: SLF001
    assert num_weeks == len(start_dates)
    for expected, date in zip(expected_start_dates, start_dates):
        assert date == expected


def test_get_week_start_dates_with_end_prior_to_start() -> None:
    """Get week starting dates where the end is prior to the start."""
    start, end = "2024-02-01", "2024-01-01"
    start_dates = api._get_week_start_dates(start, end)  # noqa: SLF001
    assert start_dates[0] == start


def test_get_week_start_dates_with_end_less_than_one_week() -> None:
    """Get week starting dates where the end is less than 7 days from the start."""
    start, end = "2024-04-08", "2024-04-13"
    start_dates = api._get_week_start_dates(start, end)  # noqa: SLF001
    assert start_dates[0] == "2024-04-08"


_schedule_endpoint_matcher = re.compile(rf"{api.URL}/schedule/.*")


def test_get_schedule_for_all_teams_now(
    mock_aioresponse: aioresponses, ep_match_schedule: re.Pattern[AnyStr]
) -> None:
    """Test getting the current schedule for all teams."""
    resp = {"foo": "bar"}
    mock_aioresponse.get(ep_match_schedule, payload=resp)
    for s in api.get_weekly_schedules():
        assert s == resp


def test_get_schedule_for_date(
    mock_aioresponse: aioresponses,
    ep_match_schedule: re.Pattern[AnyStr],
) -> None:
    """Test getting the schedule for all teams on a specific date."""
    resp = {"foo": "bar"}
    datestr = "2024-01-01"
    mock_aioresponse.get(ep_match_schedule, payload=resp)
    assert all(s == resp for s in api.get_weekly_schedules(datestr))


def test_get_schedule_with_bad_date_raises() -> None:
    """Test that an incorrect date supplied ot get_schedule raises value error."""
    datestr = "not-a-date"
    with pytest.raises(
        ValueError, match=f"time data {datestr!r} does not match format '%Y-%m-%d'"
    ):
        api.get_weekly_schedules(date_from=datestr)


def test_get_weekly_schedule_with_sample_data(
    mock_aioresponse: aioresponses,
    ep_match_schedule: re.Pattern[AnyStr],
    schedule_data: list[dict[str, Any]],
) -> None:
    """Get weekly schedule with actuals sample data."""
    mock_aioresponse.get(ep_match_schedule, payload=schedule_data)
    schedule = next(api.get_weekly_schedules("2024-01-01"))
    assert len(schedule)
    assert isinstance(schedule, dict)
    assert "gameWeek" in schedule
    assert len(schedule["gameWeek"]) == 7


def test_get_game_info_for_single_game_id(
    mock_aioresponse: aioresponses,
    ep_match_game: re.Pattern[AnyStr],
) -> None:
    """Returns info for a single game."""
    mock_aioresponse.get(ep_match_game, payload={"foo": "bar"})
    game_info = api.get_game_info(2023020721)
    assert next(game_info)["foo"] == "bar"


def test_get_game_info_returns_empty_with_api_error_response(
    mock_aioresponse: aioresponses,
    ep_match_game: re.Pattern[AnyStr],
) -> None:
    """Fails when unable to get valid response from API."""
    mock_aioresponse.get(ep_match_game, payload={"foo": "bar"}, status=404)
    game_info = api.get_game_info(2023020721)
    with pytest.raises(StopIteration):
        next(game_info)


@pytest.mark.asyncio
async def test_can_run_in_thread(
    mock_aioresponse: aioresponses,
    ep_match_game: re.Pattern[AnyStr],
) -> None:
    """Runs with a new event loop in another thread."""
    mock_aioresponse.get(ep_match_game, payload={"foo": "bar"}, repeat=True)
    game_info = list(api.get_game_info([20230207011, 20230207012]))
    assert len(game_info) == 2
