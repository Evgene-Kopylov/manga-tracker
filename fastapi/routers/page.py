from typing import Dict, Any

from fastapi import APIRouter, Request

from db.models import Page
from db.schemas.page import AddPageSchema
from db.session import SessionLocal
from routers.page_utils import get_name

session = SessionLocal()
router = APIRouter()


@router.post('/page')
def user_registration(request: Request, page: AddPageSchema
                      ) -> Dict[str, Any]:
    p = Page()
    p.url = page.url
    p.element = page.element
    p.block = page.block
    session.add(p)
    session.commit()
    my_header = request.headers.get('api-key')
    return {
        'msg': 'page added.',
        'api-key': my_header
    }


@router.get('/add_page')
def add_page(url: str, element: str, block: str
             ) -> Dict[str, Any]:
    page = Page()
    page.url = url
    page.element = element
    page.block = block
    page.name = get_name(url)
    session.add(page)
    session.commit()
    return {
        'msg': f'{page.id=} added.',
        'url': url[:100] or url,
        'name': page.name,
        'element': ('... ' + element[-50:]) or element,
        'block': ('... ' + block[-50:]) or block,
    }
