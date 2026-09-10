from pathlib import Path
import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def load_config(config_path: str | Path | None = None) -> dict:
    """Load the yaml config and flip it into an extension -> folder lookup,
    which is a lot more useful at sort-time than the folder -> extensions
    shape it's written in (that shape is just nicer for humans to edit)."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH

    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    extension_map = {}
    for folder, extensions in raw.get("categories", {}).items():
        for ext in extensions:
            extension_map[ext.lower()] = folder

    return {
        "extension_map": extension_map,
        "fallback_folder": raw.get("fallback_folder", "Other"),
    }
