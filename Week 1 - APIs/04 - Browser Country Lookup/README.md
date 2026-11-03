# Browser Country Lookup

## Purpose

Practice calling the REST Countries API directly from a web browser using JavaScript's `fetch()` function.

## File

- `day4_fetch.html` — provides a simple country search page and displays country information returned by the API.

## Run

Open `day4_fetch.html` in a browser, enter a country name, and select **Search**. The page also supports pressing Enter.

No Python package is required for this HTML exercise. The shared environment remains available for the other projects in this repository.

## Learning points

- Calling an API from browser JavaScript
- Using `fetch()` and `async/await`
- Encoding user input for a URL
- Handling unsuccessful HTTP responses
- Displaying API response data in a web page

## Security note

The current HTML exercise contains a demonstration credential in the request header. Do not replace it with a real private API key in browser code: credentials embedded in client-side HTML/JavaScript are visible to users. A production implementation should make authenticated requests through a backend.
