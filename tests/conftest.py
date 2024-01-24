"""PyTest fixtures."""
from datetime import date
from datetime import time
from typing import Any

import pytest

from yohonhl import stats


@pytest.fixture()
def linescore_data() -> tuple[dict[Any, Any], list[stats.Goal]]:
    """Fixture for linescore and corresponding goal data."""
    goals = [
        stats.Goal(
            season=20232024,
            game_id=2023020718,
            game_date=date(2024, 1, 21),
            period=1,
            time_in_period=time(0, 11, 57),
            player_name="E. Zamula",
            player_team="PHI",
            home_team="PHI",
            away_team="OTT",
            home_score=1,
            away_score=0,
            strength="PP",
        ),
        stats.Goal(
            season=20232024,
            game_id=2023020718,
            game_date=date(2024, 1, 21),
            period=1,
            time_in_period=time(0, 16, 40),
            player_name="E. Zamula",
            player_team="PHI",
            home_team="PHI",
            away_team="OTT",
            home_score=2,
            away_score=0,
            strength="EV",
        ),
    ]
    resp_data = {
        "games": [
            {
                "id": 2023020718,
                "season": 20232024,
                "gameDate": goals[0].game_date.strftime("%Y-%m-%d"),
                "gameState": "OFF",
                "awayTeam": {
                    "abbrev": "OTT",
                },
                "homeTeam": {
                    "abbrev": "PHI",
                },
                "goals": [
                    {
                        "period": g.period,
                        "timeInPeriod": g.time_in_period.strftime("%M:%S"),
                        "name": {
                            "default": g.player_name,
                        },
                        "teamAbbrev": g.player_team,
                        "awayScore": g.away_score,
                        "homeScore": g.home_score,
                        "strength": g.strength,
                    }
                    for g in goals
                ],
            },
            {
                "id": 2023020719,
                "season": 20232024,
                "gameDate": "2024-01-21",
                "gameState": "LIVE",
                "gameScheduleState": "OK",
                "awayTeam": {
                    "abbrev": "MIN",
                },
                "homeTeam": {
                    "abbrev": "CAR",
                },
            },
            {
                "id": 2023020719,
                "season": 20232024,
                "gameDate": "2024-01-21",
                "gameState": "OFF",
                "gameScheduleState": "OK",
                "awayTeam": {
                    "abbrev": "MIN",
                },
                "homeTeam": {
                    "abbrev": "CAR",
                },
            },
        ],
    }
    return resp_data, goals
