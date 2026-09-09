from pathlib import Path

import pytest

from organizer.config import load_config
from organizer.sorter import sort_directory, plan_moves, IGNORED_NAMES


@pytest.fixture
def config():
    return load_config()


def touch(path: Path, name: str):
    (path / name).write_text("placeholder")


def test_sorts_known_extensions_into_matching_folders(tmp_path, config):
    touch(tmp_path, "photo.jpg")
    touch(tmp_path, "notes.txt")
    touch(tmp_path, "script.py")

    sort_directory(tmp_path, config)

    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "notes.txt").exists()
    assert (tmp_path / "Code" / "script.py").exists()


def test_unknown_extension_goes_to_fallback_folder(tmp_path, config):
    touch(tmp_path, "mystery.xyz")

    sort_directory(tmp_path, config)

    assert (tmp_path / "Other" / "mystery.xyz").exists()


def test_dry_run_does_not_move_anything(tmp_path, config):
    touch(tmp_path, "photo.jpg")

    sort_directory(tmp_path, config, dry_run=True)

    assert (tmp_path / "photo.jpg").exists()
    assert not (tmp_path / "Images").exists()


def test_existing_subfolders_are_skipped(tmp_path, config):
    (tmp_path / "Images").mkdir()
    touch(tmp_path / "Images", "already_sorted.jpg")

    moves = plan_moves(tmp_path, config)

    assert moves == []


def test_name_collision_gets_suffixed_instead_of_overwritten(tmp_path, config):
    (tmp_path / "Documents").mkdir()
    (tmp_path / "Documents" / "notes.txt").write_text("original file, don't touch")
    touch(tmp_path, "notes.txt")

    sort_directory(tmp_path, config)

    original = (tmp_path / "Documents" / "notes.txt").read_text()
    assert original == "original file, don't touch"
    assert (tmp_path / "Documents" / "notes (1).txt").exists()


def test_ignored_files_are_left_alone(tmp_path, config):
    for name in IGNORED_NAMES:
        touch(tmp_path, name)

    moves = plan_moves(tmp_path, config)

    assert moves == []
    for name in IGNORED_NAMES:
        assert (tmp_path / name).exists()


def test_hidden_files_are_left_alone(tmp_path, config):
    touch(tmp_path, ".hidden_config")

    moves = plan_moves(tmp_path, config)

    assert moves == []
