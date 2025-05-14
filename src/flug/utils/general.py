from pathlib import Path


def get_storage_dir():
    return Path(Path.home() / ".local/share" / "flug")
