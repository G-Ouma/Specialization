# Poultry Egg Production Tracker — REST API

## Overview

A Flask application for recording and viewing daily egg-production counts across poultry sheds. It provides a browser interface and a JSON API.

The current implementation stores records in a Python list in memory. Records are lost when the server restarts.

## Features

- Submit a production record containing shed, date, and egg count.
- Validate required fields, date format, and non-negative integer counts.
- Retrieve all records in date and shed order.
- Calculate a running egg total and overall summary.
- Display records and totals in the browser interface.

## Technology and structure

- Python and Flask
- HTML, CSS, and browser JavaScript
- JSON over HTTP

```text
REST API/
├── main.py
├── requirements.txt
└── templates/
    └── index.html
```

## Setup and run

From this project folder, install the dependencies:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Open the local address printed by Flask, normally `http://127.0.0.1:5000`.

## API endpoints

### Add a production record

`POST /api/eggs`

Send JSON with all three fields:

```json
{
  "shed": "Shed A",
  "date": "2026-11-20",
  "count": 250
}
```

The date must use `YYYY-MM-DD` format. The count must be a non-negative integer. A successful request returns HTTP 201 and the saved record. Missing or invalid data returns HTTP 400 with an error message.

### Retrieve production records

`GET /api/eggs`

Returns a JSON response containing:

- `records` — records sorted by date and shed, each with a running total.
- `total_records` — number of records stored.
- `total_eggs` — sum of all recorded egg counts.

## Browser interface

The home page provides a form to submit a shed, production date, and egg count. It fetches the current records from `GET /api/eggs`, displays the totals, and refreshes the table after a successful submission.

## Limitations and next steps

- Records are held in memory and disappear on restart.
- There is no database, authentication, or user-role management.
- The running total is calculated across the sorted record list, not separately per shed.
- There are no update or delete endpoints.

Possible next steps include persistent database storage, per-shed summaries, filtering by date range, authentication, and automated API tests.
