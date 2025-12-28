# htmltopdf-api

A simple FastAPI REST application to run wkhtmltopdf.

## Installation

### Docker
Use the provided Dockerfile or the built image at `ghcr.io/matbyte-com/htmltopdf-api`.

**Supported Architectures:**
- `linux/amd64` (x86_64)
- `linux/arm64` (aarch64)

Available tags:
- `latest` - Latest build from the main branch
- `a.b.c` - Semantic version tags (e.g., `1.0.0`, `1.0`, `1`)
- `<branch>-<sha>` - Branch-specific builds with git SHA
- `<branch>` - Latest build from a specific branch

All images are multi-architecture and will automatically pull the correct version for your platform.

### Virtual Environment

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python3 main.py`

## Usage
Once the API is running, it can be accessed on port 9090.

Swagger docs can be found at `/docs`. A healthcheck endpoint is available at `/healthz`.

`POST /v1/convert`

```json
{
  "html": "<html><b>Test</b></html>",
  "options": {
    "grayscale": true,
    ...
  }
}
```

## Testing

Run the test suite with pytest:

```bash
pytest -v
```

Or run tests with coverage:

```bash
pytest --cov=main --cov-report=html
```

## CI/CD

This project uses GitHub Actions for continuous integration and deployment:

- **Tests**: Run automatically on every push and pull request on both AMD64 and ARM64 architectures
- **Docker Images**: Multi-architecture images (linux/amd64, linux/arm64) built and pushed to GitHub Container Registry only after tests pass on both architectures
- **Tagging**: Images are automatically tagged with:
  - Git branch name
  - Git SHA
  - Semantic version tags in format `a.b.c` (e.g., `1.0.0`, `1.0`, `1`)
  - `latest` tag for the default branch
