# htmltopdf-api

A simple FastAPI REST application to run wkhtmltopdf.

## Installation

### Docker
Use the provided Dockerfile or the built image at `ghcr.io/matbyte-com/htmltopdf-api`.

### Virtual Environment

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python3 main.py`

## Usage
Once the API is running, it can be accessed on port 9090.

Swagger docs can be found at `/docs`. A healthcheck endpoint is available at `/healthz`.

`POST /v1/convert`

```
{
  "html": "<html><b>Test</b></html>",
  "options": {
    "grayscale": true,
    ...
  }
}
```
