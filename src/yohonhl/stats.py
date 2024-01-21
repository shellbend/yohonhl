"""Stats aggregation and calculations."""

from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import time
from typing import Any

from yohonhl import api


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


def goals_from_linescores(linescores: dict[str, Any]) -> list[Goal]:
    """Get a list of goals from linescore data."""
    all_goals = []
    for game in linescores["games"]:
        if game["gameState"] != "OFF":
            continue
        game_id = int(game["id"])
        season = int(game["season"])
        game_date = datetime.strptime(game["gameDate"], "%Y-%m-%d").date()  # noqa: DTZ007
        away_team = game["awayTeam"]["abbrev"]
        home_team = game["homeTeam"]["abbrev"]
        try:
            game_goals = game["goals"]
        except KeyError:
            # Some games might not have any goals yet, e.g. in-progress games
            continue
        for goal in game_goals:
            all_goals.append(
                Goal(
                    season=season,
                    game_id=game_id,
                    game_date=game_date,
                    period=int(goal["period"]),
                    time_in_period=datetime.strptime(  # noqa: DTZ007
                        goal["timeInPeriod"], "%M:%S"
                    ).time(),
                    player_name=goal["name"]["default"],
                    player_team=goal["teamAbbrev"],
                    home_team=home_team,
                    away_team=away_team,
                    home_score=int(goal["homeScore"]),
                    away_score=int(goal["awayScore"]),
                    strength=goal["strength"],
                )
            )
    return all_goals


def get_goals() -> list[Goal]:
    """Get a list of all goals from current linescores."""
    ls = api.get_linescores()
    return goals_from_linescores(ls)
