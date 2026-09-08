import logging
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from organizer.sorter import sort_directory

logger = logging.getLogger("organizer")


class _SortOnCreateHandler(FileSystemEventHandler):
    def __init__(self, directory: Path, config: dict, dry_run: bool):
        self.directory = directory
        self.config = config
        self.dry_run = dry_run

    def on_created(self, event):
        if event.is_directory:
            return
        # small delay so we're not grabbing a file mid-download/mid-copy
        time.sleep(1)
        sort_directory(self.directory, self.config, dry_run=self.dry_run)

    def on_moved(self, event):
        # covers browsers that download to a .part/.tmp name and rename
        # once the download finishes
        self.on_created(event)


def watch_directory(directory: str | Path, config: dict, dry_run: bool = False) -> None:
    directory = Path(directory)
    handler = _SortOnCreateHandler(directory, config, dry_run)

    observer = Observer()
    observer.schedule(handler, str(directory), recursive=False)
    observer.start()

    logger.info("watching %s (ctrl-c to stop)", directory)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("stopped watching")
    observer.join()
