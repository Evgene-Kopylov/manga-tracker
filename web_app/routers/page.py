import os
from typing import Dict, Any

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

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
             ) -> RedirectResponse:
    page = Page()
    page.url = url
    page.element = element
    page.block = block
    page.name = get_name(url)
    duble = session.query(Page).filter_by(
        url=page.url
    ).first()
    if not duble:
        session.add(page)
        page.pending = True
        session.commit()
        publisher.publish('new_page', str(page.id))
    else:
        print('page duplicate')

    return RedirectResponse('/')
