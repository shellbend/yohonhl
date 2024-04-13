"""NHL API functions.

[1]: https://github.com/Zmalski/NHL-API-Reference#get-game-information-1
[2]: https://gitlab.com/dword4/nhlapi/-/blob/master/new-api.md
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Coroutine
from typing import Iterable
from typing import Iterator
from typing import Sequence
from typing import Union

import aiohttp

URL = "https://api-web.nhle.com/v1"

DATE_FMT = "%Y-%m-%d"

_log = logging.getLogger("yohonhl.api")


def parse_date(datestr: str) -> date:
    """Parse a date string from the API into a naive datetime.date object."""
    return datetime.strptime(datestr, DATE_FMT).date()  # noqa: DTZ007


def fmt_date(d: date) -> str:
    """Format a datetime.date into YYYY-MM-DD for the API."""
    return d.strftime(DATE_FMT)


def normalize_datestr(datestr: str) -> str:
    """Normalize a datestring into YYYY-MM-DD."""
    return datetime.strftime(datetime.strptime(datestr, DATE_FMT), DATE_FMT)  # noqa: DTZ007


def _get_week_start_dates(date_from: str, date_to: str) -> Sequence[str]:
    """Get start dates for schedule requests between two given dates."""
    dt_from, dt_to = parse_date(date_from), parse_date(date_to)
    num_days = (dt_to - dt_from).days
    num_weeks = num_days // 7 + 1
    if num_days > 0:
        dts_start = [dt_from + i * timedelta(days=7) for i in range(num_weeks)]
    else:
        dts_start = [dt_from]
    _log.debug(
        "Week start dates for %s - %s (%d days): %r",
        dt_from,
        dt_to,
        num_days,
        dts_start,
    )
    return [fmt_date(d) for d in dts_start]


async def _get_endpoint_async(url: str, session: aiohttp.ClientSession) -> Any:
    async with session.get(url=url) as response:
        _log.debug("GET %r -> status: %r", response.url, response.status)
        if response.ok:
            return await response.json()
        return None


async def _get_endpoints_async(urls: Iterable[str]) -> Iterator[dict[str, Any]]:
    """Get multiple endpoints in parallel."""
    async with aiohttp.ClientSession() as session:
        tasks = (_get_endpoint_async(url, session) for url in urls)
        results = await asyncio.gather(*tasks)
        return filter(None, results)


def _run_async(coro: Coroutine[Any, Any, Iterable[dict[str, Any]]]) -> Any:
    """Run asyncio in a thread if an event loop is already running.

    This is necessary to allow running async functions from a Jupyter Notebook,
    which has a running asyncio event loop.
    """
    try:
        asyncio.get_running_loop()
        with ThreadPoolExecutor(1) as pool:

            def job() -> Any:
                return asyncio.run(coro)

            return pool.submit(job).result()
    except RuntimeError:
        return asyncio.run(coro)


def get_weekly_schedules(
    date_from: str = "", date_to: str = ""
) -> Iterator[dict[str, Any]]:
    """Get the weekly schedule of games between given dates."""
    if not date_from:
        return _run_async(_get_endpoints_async([f"{URL}/schedule/now"]))  # type: ignore

    date_from = normalize_datestr(date_from)
    date_to = date_from if not date_to else normalize_datestr(date_to)
    start_dates = _get_week_start_dates(date_from, date_to)

    _log.debug("Getting weekly schedules for %r", start_dates)
    urls = (f"{URL}/schedule/{dt}" for dt in start_dates)
    return _run_async(_get_endpoints_async(urls))  # type: ignore


def get_game_info(game_ids: Union[int, list[int]]) -> Iterator[dict[str, Any]]:
    """Get game info with parallel API requests using aiohttp."""
    if isinstance(game_ids, int):
        game_ids = [game_ids]
    urls = (f"{URL}/gamecenter/{g}/landing" for g in game_ids)
    return _run_async(_get_endpoints_async(urls))  # type: ignore
