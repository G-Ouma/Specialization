# Legal Client File Sorter

## Overview

A Python command-line utility that organizes files directly inside a target folder into subfolders based on their file extensions. It is demonstrated with a dummy client-document folder intended to resemble a law firm's working documents.

The script processes files in the target folder's top level only. It does not recursively sort files already inside subfolders.

## File categories

| Destination folder | Extensions |
|---|---|
| `Contracts` | `.doc`, `.docx` |
| `Evidence` | `.jpg`, `.jpeg`, `.png` |
| `Filings` | `.pdf` |
| `Correspondence` | `.txt`, `.eml` |
| `Other` | All other extensions |

Extension matching is case-insensitive, so files such as `court_order.PDF` are categorized as filings.

## Features

- Creates category folders when needed.
- Moves files using `shutil.move`.
- Avoids overwriting existing files by adding suffixes such as `_1` and `_2` to duplicate destination names.
- Appends a timestamp, original path, and destination path to `sort_log.txt`.
- Skips the log file and does not process existing subfolder contents.
- Reports the number of successfully moved files.

## Requirements

- Python 3
- No third-party packages; the script uses the Python standard library.

## Run

From this folder:

```powershell
python sort_files.py "C:\Path\To\TargetFolder"
```

Replace the example path with the folder you want to organize. The target folder must already exist.

## Test with the sample documents

The `dummy_client_documents` directory contains 12 dummy files across the five categories. Run:

```powershell
python sort_files.py ".\dummy_client_documents"
```

The first run organizes the top-level sample files into category folders. Subsequent runs do not re-sort files already inside those folders.

## Log

The script creates or appends to:

```text
TARGET_FOLDER/
└── sort_log.txt
```

Each successful move is recorded with a local timestamp, source path, and destination path. Failed moves are printed to standard error.

## Safety notes

Test on copies or dummy documents before using the script on important client records. The utility moves files rather than copying them, and it does not provide undo or transactional rollback. Keep the generated log if you need a record of the moves.

## Files

- `sort_files.py` — command-line sorter.
- `dummy_client_documents/` — sample files for testing.
- `README.md` — usage and behaviour documentation.
