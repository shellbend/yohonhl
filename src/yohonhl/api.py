"""NHL API functions."""

from datetime import datetime
from enum import Enum
from typing import Any

import requests

URL = "https://api-web.nhle.com/v1"


class DateStr(Enum):
    """Date strings used in API requests."""

    WEEK = "week"
    MONTH = "month"
    NOW = "now"


def get_team_schedule(
    team_abbrev: str, datestr: DateStr = DateStr.NOW, timeout: float = 5
) -> Any:
    """Get the schedule for a single team."""
    if datestr == DateStr.NOW:
        url = f"{URL}/club-schedule-season/{team_abbrev}/now"
    else:
        url = f"{URL}/club-schedule/{team_abbrev}/{datestr.value}"
    return requests.get(url, timeout=timeout).json()


def get_schedule(datestr: str = DateStr.NOW.value, timeout: float = 5) -> Any:
    """Get the schedule for all teams."""
    if isinstance(datestr, str) and datestr != "now":
        fmt = "%Y-%m-%d"
        datestr = datetime.strftime(
            datetime.strptime(datestr, fmt),  # noqa: DTZ007
            fmt,
        )
    return requests.get(f"{URL}/schedule/{datestr}", timeout=timeout).json()


def get_linescores(timeout: float = 5) -> Any:
    """Get linescore details."""
    return requests.get(f"{URL}/score/now", timeout=timeout).json()


def get_boxscores(game_id: int, timeout: float = 5) -> Any:
    """Get the boxscore for a game."""
    return requests.get(f"{URL}/gamecenter/{game_id}/boxscore", timeout=timeout).json()
