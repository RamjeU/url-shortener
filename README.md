# URL Shortener API

A lightweight REST API that shortens long URLs, redirects short codes to their
original destination, and tracks click counts — built with Flask and SQLite.

## Features

- `POST /api/shorten` — turn a long URL into a short code
- `GET /<code>` — redirect to the original URL
- `GET /api/stats/<code>` — view click count and creation date
- Input validation (rejects malformed URLs)
- Collision-safe short code generation
- SQLite persistence (zero external DB setup)
- Test suite with `pytest`

## Tech Stack

- Python 3.11+
- Flask
- SQLite3 (standard library)
- pytest

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── database.py      # SQLite connection + schema
│   └── routes.py        # API endpoints
├── tests/
│   └── test_api.py      # pytest test suite
├── run.py                # entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

```bash
# clone and enter the repo
git clone https://github.com/RamjeU/url-shortener.git
cd url-shortener

# create a virtual environment
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the server
python run.py
```

Server runs at `http://localhost:5001`.

## API Usage

**Shorten a URL**
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/some/very/long/path"}'
```

Response:
```json
{
  "short_code": "aZ3kQ1",
  "short_url": "http://localhost:5000/aZ3kQ1",
  "original_url": "https://www.example.com/some/very/long/path"
}
```

**Visit the short URL**
```bash
curl -L http://localhost:5000/aZ3kQ1
# redirects to the original URL
```

**Check stats**
```bash
curl http://localhost:5000/api/stats/aZ3kQ1
```

Response:
```json
{
  "short_code": "aZ3kQ1",
  "original_url": "https://www.example.com/some/very/long/path",
  "clicks": 4,
  "created_at": "2026-07-01 14:32:01"
}
```

## Running Tests

```bash
pytest
```

## Possible Extensions

- Custom short codes (`POST /api/shorten` with `"custom_code": "my-link"`)
- Expiring links (TTL)
- Rate limiting per IP
- A minimal frontend form (single `index.html`)
- Swap SQLite for Postgres and deploy to Render/Railway

## License

MIT
