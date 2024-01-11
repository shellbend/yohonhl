"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """YohoNHL."""


if __name__ == "__main__":
    main(prog_name="yohonhl")  # pragma: no cover
