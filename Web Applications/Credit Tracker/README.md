# Credit Tracker

## Overview

A small Flask application that looks up customer credit balances for a demonstration hardware business. The browser sends a customer-name search to a backend endpoint, which searches a hard-coded Python dictionary and returns a matching balance.

## Features

- Simple customer-name search interface.
- Case-insensitive matching against the sample customer list.
- Returns a balance in Kenyan shillings when exactly one customer matches.
- Reports when a customer is not found.
- Returns an ambiguity error when multiple customers match the search.

## Technology and files

- Python
- Flask
- HTML, CSS, and browser JavaScript

```text
Credit Tracker/
├── app.py
└── templates/
    └── index.html
```

## Setup and run

Install Flask in the shared repository environment if it is not already available:

```powershell
python -m pip install flask
```

From this project folder, run:

```powershell
python app.py
```

Open the local address printed by Flask, normally `http://127.0.0.1:5000`.

## API endpoint

| Method | Path | Query parameter | Purpose |
|---|---|---|---|
| GET | `/api/balance` | `customer` | Search the sample customer list |

Example:

```text
/api/balance?customer=john
```

A unique match returns the customer name, balance, and currency. An empty query returns HTTP 400, multiple matches return HTTP 409, and no match returns HTTP 404.

## Important limitations

- Customer names and balances are hard-coded sample data.
- Data is not stored in a database and cannot be updated through the interface.
- There is no authentication or authorization.
- Searching by a partial name can return multiple matches.
- The app is not suitable for real customer financial information.

A production version would require a secure database, authenticated access, audit logging, input and access controls, and appropriate privacy safeguards.
