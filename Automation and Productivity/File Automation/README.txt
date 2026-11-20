# Legal Client File Sorter

## Run it
```powershell
python sort_files.py "C:\Path\To\TargetFolder"
```

The script sorts files directly inside the target folder (not nested folders) into:
- `Contracts`: `.docx`, `.doc`
- `Evidence`: `.jpg`, `.jpeg`, `.png`
- `Filings`: `.pdf`
- `Correspondence`: `.txt`, `.eml`
- `Other`: all other file types

It appends a timestamp, original path, and destination path to `sort_log.txt`.
It does not overwrite same-named files: it adds `_1`, `_2`, etc. to the moved copy.
The log file itself and existing subfolder contents are not processed.

## Test
The `dummy_client_documents` folder contains 12 dummy files across all five categories.
Run the command above using that folder path to repeat the test.
