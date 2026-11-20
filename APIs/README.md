# API Projects

This folder contains four introductory exercises focused on consuming external APIs from Python and browser JavaScript.

## Projects

| Project | Description |
|---|---|
| [01 - API Basics](01%20-%20API%20Basics/README.md) | Send REST Countries requests and inspect country data |
| [02 - Weather API](02%20-%20Weather%20API/README.md) | Retrieve current weather from OpenWeather |
| [03 - Travel Information API](03%20-%20Travel%20Information%20API/README.md) | Combine weather and country information and save a local search history |
| [04 - Browser Country Lookup](04%20-%20Browser%20Country%20Lookup/README.md) | Search for country information from a browser using JavaScript `fetch()` |

## Shared Python setup

The Python exercises use the shared virtual environment and root dependency file. From the repository root, activate `venv` and install dependencies as described in the [main README](../README.md).

Create a root `.env` file from `.env.example` and add the API keys required by each script:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
REST_COUNTRIES_API_KEY=your_rest_countries_api_key
```

Do not commit real credentials. The browser exercise uses a demonstration authorization value in its HTML; never place a private API key in client-side code.

## Skills practised

- HTTP GET requests, query parameters, and request headers
- HTTP status codes, timeouts, and error handling
- JSON parsing and nested response fields
- Environment variables and API credentials
- Combining data from more than one API
- Writing structured JSON history files
- Browser-side requests with `fetch()` and `async/await`

See each project README for its exact run command and current implementation details.
