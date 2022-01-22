from typing import Dict, Any, Optional

from fastapi import APIRouter, Header, Request
from werkzeug.security import generate_password_hash

from db.models import Page
from db.schemas.page import AddPageSchema
from db.session import SessionLocal

session = SessionLocal()
router = APIRouter()


@router.post('/add_page')
def user_registration(request: Request, p: AddPageSchema) -> Dict[str, Any]:
    page = Page()
    page.url = p.url
    page.element = p.element
    page.block = p.block
    session.add(page)
    session.commit()
    my_header = request.headers.get('api-key')
    return {
        'msg': 'page added.',
        'api-key': my_header
    }
