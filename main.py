from fastapi import FastAPI

import users, auth

app = FastAPI()

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


@app.exception_handler(ValidationError)
async def validation_exception_handler(_, exc: ValidationError):
    return JSONResponse({"detail": exc.errors().pop()["msg"]}, status_code=400)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse({"detail": exc.errors()}, status_code=400)


app.add_exception_handler
app.include_router(auth.router)
app.include_router(users.router, prefix="/users")
