# TodoMVC Playwright Tests

Automated tests (Playwright + pytest, Python) for https://demo.playwright.dev/todomvc/

## Setup

Requires Python 3 (developed with 3.14).

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
pytest                 # headless
pytest --headed        # watch the browser
pytest -k delete       # run tests matching a name
```

pytest may print a `PytestRemovedIn10Warning`. It comes from the
`pytest-playwright` plugin itself, not from these tests, and does not affect results.
