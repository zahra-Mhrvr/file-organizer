import logging

import click

from organizer.config import load_config
from organizer.sorter import sort_directory
from organizer.watcher import watch_directory


def _setup_logging(verbose: bool):
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(asctime)s  %(message)s",
        datefmt="%H:%M:%S",
    )
    # always show info-level for our own logger, regardless of -v,
    # otherwise running this thing feels like it's doing nothing
    logging.getLogger("organizer").setLevel(logging.INFO)


@click.group()
def cli():
    """Sort a messy folder into subfolders by file type."""
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--config", "config_path", default=None, help="Path to a custom config.yaml")
@click.option("--dry-run", is_flag=True, help="Show what would happen without moving anything")
@click.option("-v", "--verbose", is_flag=True)
def sort(directory, config_path, dry_run, verbose):
    """Sort DIRECTORY once and exit."""
    _setup_logging(verbose)
    config = load_config(config_path)
    moves = sort_directory(directory, config, dry_run=dry_run)

    if not moves:
        click.echo("nothing to sort, folder's already clean")
    elif dry_run:
        click.echo(f"would move {len(moves)} file(s), run without --dry-run to actually do it")
    else:
        click.echo(f"moved {len(moves)} file(s)")


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--config", "config_path", default=None, help="Path to a custom config.yaml")
@click.option("--dry-run", is_flag=True, help="Log what would happen without moving anything")
def watch(directory, config_path, dry_run):
    """Keep watching DIRECTORY and sort new files as they show up."""
    _setup_logging(verbose=True)
    config = load_config(config_path)
    watch_directory(directory, config, dry_run=dry_run)


if __name__ == "__main__":
    cli()
