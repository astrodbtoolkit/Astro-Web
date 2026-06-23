# Astro-Web Tests

This directory contains the test suite for the Astro-Web application. The tests are designed to ensure the reliability of astronomical database queries, API endpoints, and web page rendering.

## Test Organization

The tests are split into two main categories:

- **`unit/`**: Isolated tests for utility functions and visualization logic that do not require a database connection.
  - `database/`: Tests for coordinate parsing and unit conversions.
  - `visualizations/`: Tests for Bokeh plot generation logic.
- **`integration/`**: Tests that verify the interaction between different components, including the database and the web framework.
  - `api/`: Verifies RESTful API endpoints and JSON responses.
  - `database/`: Verifies data retrieval using `astrodbkit` from the SQLite database.
  - `web/`: Verifies that Jinja2 templates render correctly with live data.

## Requirements

### Database
Integration tests require a copy of the **astrodb-template** database in the project root.
- **File name**: `astrodb-template.sqlite`
- **Download**: You can download the latest version from [astrodbtoolkit/astrodb-template-db](https://github.com/astrodbtoolkit/astrodb-template-db/raw/main/astrodb-template.sqlite).

The tests expect this file to be present at the path specified by `ASTRO_WEB_DATABASE_URL` (defaults to `sqlite:///astrodb-template.sqlite`).

> **Note**: The template database has no `Spectra` rows, so spectra-dependent tests are marked `xfail` (expected to fail).

### Environment
Configuration is read from environment variables (see `astro_web/config.py`). Copy `.env.example` to `.env` so the integration tests resolve the correct database path and column names (e.g. `ra_deg`/`dec_deg`):
```bash
cp .env.example .env
```

### Dependencies
All testing dependencies are included in the `dev` optional dependency group in `pyproject.toml`.

## Running Tests

### Using `uv` (Recommended)
To run the full test suite:
```bash
uv run pytest
```

To run with coverage report:
```bash
uv run pytest --cov
```

### Running Specific Tests
You can target specific directories or files:
```bash
# Run only unit tests
uv run pytest tests/unit

# Run only database integration tests
uv run pytest tests/integration/database
```

## Continuous Integration
Tests are automatically run on GitHub Actions for every push and pull request to the `main` branch. The CI environment automatically downloads the required database to perform integration testing.
