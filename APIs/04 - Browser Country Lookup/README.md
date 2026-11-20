# Browser Country Lookup

## Purpose

A small browser-based exercise for searching country information using the REST Countries API and JavaScript's `fetch()` function.

## File

- `day4_fetch.html` — contains the search interface and JavaScript that requests a country by common name, then displays its flag, capital, region, and population.

## Run

Open `day4_fetch.html` in a modern web browser. Enter a country name and select **Search**. Pressing Enter in the input field also starts the lookup.

No Python server or package is required for this exercise.

## Concepts practised

- Browser-side HTTP requests with `fetch()`
- `async/await` and promise-based request handling
- Encoding user input for a URL
- Checking `response.ok` and handling unsuccessful responses
- Updating page content with returned JSON data

## Credential and security note

The current exercise includes a demonstration authorization value in the HTML. It is not a private key. Do not put a real secret in browser HTML or JavaScript: anyone using the page can inspect client-side code and network requests. A production application that requires a private credential should make the authenticated API request through a backend.

## Limitations

This is a single-page learning exercise. It does not include a backend, persistent search history, or automated browser tests.
