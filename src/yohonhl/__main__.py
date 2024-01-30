"""Command-line interface."""

import logging
from datetime import datetime

import click
import pandas as pd

from yohonhl import api
from yohonhl import stats


@click.group()
@click.version_option()
@click.option("-v", "--verbose", flag_value=True)
def main(verbose: bool) -> None:
    """YohoNHL."""
    logging.basicConfig()
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)


def _current_datestr() -> str:
    return api.fmt_date(datetime.now().date())  # noqa: DTZ005


@main.command()
@click.option(
    "-o",
    "--output",
    help="Write goals to output file as CSV",
    type=click.Path(dir_okay=False, writable=True, allow_dash=True),
    default="-",
)
@click.option(
    "-a",
    "--append",
    help="Append to the output file if it exists.",
    is_flag=True,
    default=False,
)
@click.option(
    "-f",
    "--from",
    "start",
    help="Get goals starting from date (YYYY-MM-DD).",
    default=_current_datestr(),
    show_default=True,
)
@click.option(
    "-t",
    "--to",
    "end",
    help="End date for range from which to get goals (YYYY-MM-DD). "
    "Ignored if --from is not specified as well.",
    default=_current_datestr(),
    show_default=True,
)
def goals(output: str, append: bool, start: str, end: str) -> None:
    """Get goal data for games."""
    goals = stats.get_goals(start_date=start, end_date=end)
    df = pd.DataFrame(goals)  # type: ignore
    with click.open_file(output, mode="a" if append else "w") as f:
        df.to_csv(f, index=False, header=not append)


if __name__ == "__main__":
    main(prog_name="yohonhl")  # pragma: no cover
