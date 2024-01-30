"""Stats aggregation and calculations."""

import logging
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import time
from itertools import chain
from typing import Any
from typing import Iterable

from yohonhl import api

_log = logging.getLogger("yohonhl.stats")


@dataclass
class Goal:
    """Goal dataclass."""

    season: int
    game_id: int
    game_date: date
    period: int
    time_in_period: time
    player_name: str
    player_team: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    strength: str


def _parse_goals_from_game_info(info: dict[str, Any]) -> list[Goal]:
    """Get a list of all goals from a given game info object."""
    season = info["season"]
    game_date = api.parse_date(info["gameDate"])
    home_team = info["homeTeam"]["abbrev"]
    away_team = info["awayTeam"]["abbrev"]

    try:
        scoring = info["summary"]["scoring"]
    except KeyError:
        # Game may be incomplete, and thus have no summary/scoring.
        _log.warning(
            "No scores yet for %s: %s @ %s on %s",
            info["id"],
            away_team,
            home_team,
            game_date,
        )
        return []

    all_goals = []
    for period in scoring:
        goal_period = int(period["period"])
        for goal in period["goals"]:
            all_goals.append(
                Goal(
                    season=season,
                    game_id=info["id"],
                    game_date=game_date,
                    period=goal_period,
                    time_in_period=datetime.strptime(  # noqa: DTZ007
                        goal["timeInPeriod"], "%M:%S"
                    ).time(),
                    player_name=goal["name"]["default"],
                    player_team=goal["teamAbbrev"]["default"],
                    home_team=home_team,
                    away_team=away_team,
                    home_score=int(goal["homeScore"]),
                    away_score=int(goal["awayScore"]),
                    strength=goal["strength"],
                    # assists=[a["name"]["default"] for a in goal["assists"]],
                )
            )
    return all_goals


def _date_opt(optstr: str) -> tuple[date, str]:
    dt = datetime.now().date() if not optstr else api.parse_date(optstr)  # noqa: DTZ005
    return dt, api.fmt_date(dt)


def get_games(start_date: str = "", end_date: str = "") -> Iterable[dict[str, Any]]:
    """Get all games between a range of dates.

    Parameters
    ----------
    start_date, end_date : str
        Start/end dates formatted as YYYY-MM-DD. Defaults to current date.

    Returns
    -------
    Iterable[dict[str, Any]]
        Iterable of game info dictionaries.
    """
    dt_from, start_date = _date_opt(start_date)
    dt_to, end_date = _date_opt(end_date)

    if dt_to < dt_from:
        _log.warning(
            "End date must be after start date; only getting games for %s", start_date
        )
        dt_to = dt_from

    _log.debug("Getting games from %r to %r", dt_from, dt_to)

    weekly_schedules = api.get_weekly_schedules(start_date, end_date)

    return chain(
        *(
            day["games"]
            for week in weekly_schedules
            for day in week["gameWeek"]
            if api.parse_date(day["date"]) <= dt_to
        )
    )


def get_goals(start_date: str, end_date: str = "") -> Iterable[Goal]:
    """Get a list of all goals between specified dates.

    Parameters
    ----------
    start_date : str
        The starting date, in YYYY-MM-DD format
    end_date : str
        The ending date, in YYYY-MM-DD. Defaults to the current date if not specified

    Returns
    -------
    list[Goal]
        A list of `Goal` objects.
    """
    game_ids = [g["id"] for g in get_games(start_date, end_date=end_date)]
    game_info = api.get_game_info(game_ids)

    # _parse_goals_from_game_info returns a list of goals for a single game. So
    # we'll have a list of lists of goals for each game that need to be chained
    # into a single list.
    return chain(*(_parse_goals_from_game_info(i) for i in game_info))
