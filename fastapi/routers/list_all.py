from fastapi import APIRouter, Request

from db.session import SessionLocal
from fastapi.templating import Jinja2Templates


session = SessionLocal()
router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get(request: Request):
    return templates.TemplateResponse(
        "list_all.html", {"request": request})
