from pathlib import Path
from datetime import datetime
import argparse
import shutil
import sys

# File extensions are matched case-insensitively.
FOLDER_BY_EXTENSION = {
    ".docx": "Contracts",
    ".doc": "Contracts",
    ".jpg": "Evidence",
    ".jpeg": "Evidence",
    ".png": "Evidence",
    ".pdf": "Filings",
    ".txt": "Correspondence",
    ".eml": "Correspondence",
}

LOG_NAME = "sort_log.txt"


def unique_destination(destination: Path) -> Path:
    """Avoid overwriting a file when the destination name already exists."""
    if not destination.exists():
        return destination

    counter = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def sort_folder(target_folder: Path) -> int:
    """Move files directly inside target_folder into category subfolders."""
    target_folder = target_folder.expanduser().resolve()

    if not target_folder.exists() or not target_folder.is_dir():
        raise ValueError(f"Target folder does not exist or is not a folder: {target_folder}")

    log_path = target_folder / LOG_NAME
    moved_count = 0

    # Snapshot the files first. The script does not recursively process subfolders.
    files = [
        item for item in target_folder.iterdir()
        if item.is_file() and item.name != LOG_NAME
    ]

    for source in files:
        category = FOLDER_BY_EXTENSION.get(source.suffix.lower(), "Other")
        destination_folder = target_folder / category
        destination_folder.mkdir(exist_ok=True)

        destination = unique_destination(destination_folder / source.name)

        try:
            shutil.move(str(source), str(destination))
            timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
            with log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(
                    f"{timestamp} | {source} -> {destination}\n"
                )
            moved_count += 1
            print(f"Moved: {source.name} -> {category}/{destination.name}")
        except OSError as error:
            print(f"Could not move {source}: {error}", file=sys.stderr)

    print(f"\nFinished. {moved_count} file(s) moved.")
    print(f"Log saved to: {log_path}")
    return moved_count


def main():
    parser = argparse.ArgumentParser(
        description="Sort a folder of client documents into file-type subfolders."
    )
    parser.add_argument(
        "folder",
        help="Path to the folder whose files should be sorted"
    )
    args = parser.parse_args()

    try:
        sort_folder(Path(args.folder))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
