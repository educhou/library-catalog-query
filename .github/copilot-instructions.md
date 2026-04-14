# Project Guidelines

## Stack
- **Backend**: Python 3.7+ with Flask; use stdlib-only where possible (no extra deps)
- **Frontend**: Vanilla HTML5 + CSS3 + JavaScript — no React, no build tools unless explicitly requested
- **Data source**: Open Library API (`https://openlibrary.org/isbn/{isbn}.json` as primary)
- **Language**: All user-facing strings, error messages, and UI text in **Portuguese (pt-BR)**

## Architecture
- `app.py` — Flask server with API endpoints (`/api/search`, `/api/lookup-isbn`)
- `templates/index.html` — Single-page frontend, communicates with Flask via `fetch()`
- `catalog_lookup.py` — Standalone CLI for ISBN lookup (stdlib only)
- Catalog fields returned per book: ISBN, Title, Author, Publisher, Date, Subject, Abstract, Location

## Code Style

### Python
- Named constants for magic numbers and timeouts: `API_TIMEOUT = 5`, `MAX_SUBJECTS = 5`
- Use helper functions to avoid repetition — e.g. `_extract_text()` for Open Library fields that can be `str` or `{"type": ..., "value": ...}`
- Never swallow exceptions silently — always `logger.error(...)` before returning a fallback
- Validate and sanitize all inputs at the boundary (query length, ISBN format, allowed search types)
- Use `urllib.parse.quote_plus()` when interpolating user input into URLs

### JavaScript (frontend)
- Always escape user-supplied or API-supplied data before injecting into `innerHTML` — use the existing `escapeHtml()` helper
- Use `fetch()` with `.catch()` — never let network errors go unhandled

## Security Rules (enforce always)
- No `debug=True` hardcoded — read from `os.environ.get('FLASK_DEBUG', 'false')`
- No `host='0.0.0.0'` hardcoded — read from `os.environ.get('HOST', '127.0.0.1')`
- Apply rate limiting (`is_rate_limited()`) on every API endpoint before processing the request
- Validate `search_type` against an explicit whitelist (`isbn`, `title`, `author`) — reject anything else with HTTP 400
- Cap query length (max 200 chars) before forwarding to third-party APIs

## Conventions
- Do **not** create markdown summary/documentation files after changes unless the user explicitly asks
- Do **not** add comments, docstrings, or type annotations to code that was not changed
- Keep functions short and single-purpose; extract a DRY helper instead of duplicating logic across `extract_authors`, `extract_publisher`, `extract_subjects`

## Build & Run
```bash
pip install -r requirements.txt
python app.py               # dev (set FLASK_DEBUG=true for debug mode)
bash start_app.sh           # convenience wrapper
```
App runs on `http://127.0.0.1:5000` by default.
