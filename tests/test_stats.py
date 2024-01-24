"""Unit tests for yohonhl.stats module."""


from typing import Any

from yohonhl import api
from yohonhl import stats


def test_get_goals(linescore_data: Any, requests_mock: Any) -> None:
    """Test getting goals."""
    resp_data, expected_goals = linescore_data
    requests_mock.get(f"{api.URL}/score/now", json=resp_data)
    goals = stats.get_goals()
    assert len(goals) == len(expected_goals)
    for g, eg in zip(goals, expected_goals):
        assert g == eg
