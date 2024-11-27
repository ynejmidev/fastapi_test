from fastapi import FastAPI
from starlette.middleware import Middleware

from middleware.time import TimerMiddleware
import users, auth

middleware = [Middleware(TimerMiddleware)]
app = FastAPI(middleware=middleware)

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


@app.exception_handler(ValidationError)
async def validation_exception_handler(_, exc: ValidationError):
    err = exc.errors().pop()
    err["input"] = str(err["input"])  # dict "serialization"
    return JSONResponse(err, status_code=400)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_, exc: RequestValidationError):
    err = exc.errors()[0]
    err["input"] = str(err["input"])  # dict "serialization"
    return JSONResponse(err, status_code=400)


# app.add_middleware()
app.include_router(auth.router)
app.include_router(users.router, prefix="/users")
