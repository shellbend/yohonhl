"""Command-line interface."""
import click
import pandas as pd

from yohonhl import stats


@click.group()
@click.version_option()
def main() -> None:
    """YohoNHL."""


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
def goals(output: str, append: bool) -> None:
    """Get goal data for this weeks' games."""
    g = stats.get_goals()
    df = pd.DataFrame(g)
    with click.open_file(output, mode="a" if append else "w") as f:
        df.to_csv(f, index=False, header=not append)


if __name__ == "__main__":
    main(prog_name="yohonhl")  # pragma: no cover
