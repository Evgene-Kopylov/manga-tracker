import os
from typing import Dict, Any

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, Request

from db.models import Page
from db.schemas.page import AddPageSchema
from db.session import SessionLocal
from routers.page_utils import get_name
from routers.tests.rmq_pablish import Publisher


session = SessionLocal()
router = APIRouter()

load_dotenv(find_dotenv())
url = os.environ.get('AMQP_URL', "amqp://guest:guest@localhost:5672/")
rmq_config = {
    'url': url,
    'exchange': 'manga_tracker'
}
publisher = Publisher(rmq_config)


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
    duble = session.query(Page).filter_by(
        url=page.url,
        _element=page.element,
        _block=page.block
    ).first()
    if not duble:
        session.add(page)
        session.commit()
        publisher.publish('new_page', str(page.id))
    else:
        print('page duplicate')

    return {
        'id': page.id or duble.id,
        'url': url[:100] or url,
        'name': page.name,
        'element': ('... ' + element[-50:]) or element,
        'block': ('... ' + block[-50:]) or block,
        'chapters': page.chapters,
        'total': page.total,
        'new': page.new
    }
