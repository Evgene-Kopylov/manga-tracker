from typing import List

from db.models import Page
from db.session import SessionLocal

session = SessionLocal()


def get_pages() -> List:
    pages = session.query(Page).all()
    collection = [
        {
            'id': page.id,
            'url': page.url,
            'name': page.name,
            'last_chapters': page.chapters_list()[:5],
            'chapters_total': page.chapters_total(),
            'last_check': str(page.last_check),
            'last_update': str(page.last_update),
            'new': page.new
        } for page in pages
    ]
    collection.sort(key=lambda x: x['last_update'])
    return collection
