import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_healthz_returns_200(self):
        """Test that healthz endpoint returns 200 status code."""
        response = client.get("/healthz")
        assert response.status_code == 200
    
    def test_healthz_returns_healthy_message(self):
        """Test that healthz endpoint returns the correct message."""
        response = client.get("/healthz")
        assert response.json() == "Healty"


class TestConvertEndpoint:
    """Test the HTML to PDF conversion endpoint."""
    
    def test_convert_simple_html(self):
        """Test converting simple HTML to PDF."""
        data = {
            "html": "<html><body><h1>Test</h1></body></html>",
            "options": None
        }
        response = client.post("/v1/convert", json=data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert len(response.content) > 0
        # Check PDF magic number
        assert response.content[:4] == b'%PDF'
    
    def test_convert_html_with_options(self):
        """Test converting HTML to PDF with custom options."""
        data = {
            "html": "<html><body><p>Test content</p></body></html>",
            "options": {
                "page-size": "A4",
                "margin-top": "0.75in",
                "margin-right": "0.75in",
                "margin-bottom": "0.75in",
                "margin-left": "0.75in"
            }
        }
        response = client.post("/v1/convert", json=data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert len(response.content) > 0
        assert response.content[:4] == b'%PDF'
    
    def test_convert_without_options(self):
        """Test converting HTML to PDF without options."""
        data = {
            "html": "<html><body><h1>Hello World</h1><p>This is a test.</p></body></html>"
        }
        response = client.post("/v1/convert", json=data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content[:4] == b'%PDF'
    
    def test_convert_complex_html(self):
        """Test converting complex HTML with styles."""
        data = {
            "html": """
            <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        h1 { color: blue; }
                        p { color: gray; }
                    </style>
                </head>
                <body>
                    <h1>Complex Document</h1>
                    <p>This is a paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                        <li>Item 3</li>
                    </ul>
                </body>
            </html>
            """,
            "options": None
        }
        response = client.post("/v1/convert", json=data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content[:4] == b'%PDF'
    
    def test_convert_missing_html_field(self):
        """Test that missing html field returns 422 validation error."""
        data = {
            "options": None
        }
        response = client.post("/v1/convert", json=data)
        assert response.status_code == 422
    
    def test_convert_invalid_json(self):
        """Test that invalid request body returns 422."""
        response = client.post("/v1/convert", json={"invalid": "data"})
        assert response.status_code == 422

