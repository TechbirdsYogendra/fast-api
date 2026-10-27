from app.main import app
from pathlib import Path
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")
__all__ = ["app"]

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"title": "Taskboard", "request": request},
    )

