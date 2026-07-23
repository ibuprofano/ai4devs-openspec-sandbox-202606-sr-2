from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from text2gherkin.engine import convert

app = FastAPI(title="text2gherkin")


class ConvertRequest(BaseModel):
    text: str


class ConvertResponse(BaseModel):
    gherkin: str


@app.post("/convert", response_model=ConvertResponse)
def convert_endpoint(request: ConvertRequest):
    try:
        result = convert(request.text)
    except Exception as exc:
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    return ConvertResponse(gherkin=result)
