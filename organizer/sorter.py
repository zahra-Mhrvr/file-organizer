import logging
import shutil
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger("organizer")


@dataclass
class Move:
    source: Path
    destination: Path


def _destination_folder(file_path: Path, config: dict) -> str:
    ext = file_path.suffix.lower().lstrip(".")
    return config["extension_map"].get(ext, config["fallback_folder"])


def _unique_destination(dest: Path) -> Path:
    """If dest already exists, append ' (1)', ' (2)', etc instead of
    silently overwriting someone's file."""
    if not dest.exists():
        return dest

    stem, suffix, parent = dest.stem, dest.suffix, dest.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def plan_moves(directory: Path, config: dict) -> list[Move]:
    """Figure out where every file in `directory` would go, without
    actually moving anything yet. Skips subfolders and hidden files."""
    moves = []

    for item in directory.iterdir():
        if item.is_dir():
            continue
        if item.name.startswith("."):
            continue

        folder_name = _destination_folder(item, config)
        dest_dir = directory / folder_name
        dest_path = _unique_destination(dest_dir / item.name)

        moves.append(Move(source=item, destination=dest_path))

    return moves


def apply_moves(moves: list[Move], dry_run: bool = False) -> None:
    for move in moves:
        if dry_run:
            logger.info("[dry run] %s -> %s", move.source, move.destination)
            continue

        move.destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(move.source), str(move.destination))
        logger.info("moved %s -> %s", move.source, move.destination)


def sort_directory(directory: str | Path, config: dict, dry_run: bool = False) -> list[Move]:
    directory = Path(directory)
    moves = plan_moves(directory, config)
    apply_moves(moves, dry_run=dry_run)
    return moves
