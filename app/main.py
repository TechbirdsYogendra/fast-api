from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from app.core.responses import api_response
from app.database import Base, engine, ensure_owner_columns
from app.routers import auth, books, todos

#Base.metadata.create_all(bind=engine)
#ensure_owner_columns()

app = FastAPI(title="Taskboard")
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(todos.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(part) for part in error["loc"] if part != "body"),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return api_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        False,
        "Validation failed",
        errors=errors,
    )
