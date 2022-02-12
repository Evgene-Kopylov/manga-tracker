from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/test_page")
async def list_all(request: Request, chapters: str = ''):
    chapters = chapters.split(', ') if chapters else []
    return templates.TemplateResponse(
        "test_page.html", {
            "request": request,
            "chapters": chapters
        })
