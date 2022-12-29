from typing import Optional

import pdfkit as pdfkit
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel
from starlette.responses import Response

app = FastAPI()


class HTMLToPDFModel(BaseModel):
    html: str
    options: Optional[dict]


@app.get("/healthz")
def healthz():
    return "Healty"


@app.post("/v1/convert")
def html_to_pdf(data: HTMLToPDFModel = Body()):
    pdf = pdfkit.from_string(data.html, False, options=data.options)
    return Response(content=pdf, media_type="application/pdf")


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=9090, workers=2)
