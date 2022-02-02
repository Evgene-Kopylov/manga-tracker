import os
from typing import Dict, Any

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, Request

from db.models import Page
from db.schemas.page import AddPageSchema
from db.session import SessionLocal
from routers.page_utils import get_name
from routers.tests.rmq_pablish import Publisher
from routers.utils.page_static import cut_selector

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
    page = session.query(Page).filter_by(url=url, element=element, block=block).first()
    if page:
        print('page duplicate')
    else:
        page = Page()
        page.url = url
        page.element = cut_selector(element)
        page.block = cut_selector(block)
        page.name = get_name(url)
        session.add(page)
        session.commit()
        publisher.publish('new_page', str(page.id))

    return {
        'id': page.id,
        'url': url[:100] or url,
        'name': page.name,
        'element': ('... ' + element[-50:]) or element,
        'block': ('... ' + block[-50:]) or block,
        'chapters': page.chapters_list(),
        'total': page.chapters_total(),
        'new': page.new
    }
