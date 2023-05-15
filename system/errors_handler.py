from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from main import app


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()}),
    )
