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
            'last_chapters': page.chapters[:5],
            'total': page.total,
            'last_check': str(page.last_check),
            'last_update': str(page.last_update),
            'new': page.new,
            'processing': page.processing
        } for page in pages
    ]
    collection.sort(key=lambda x: x['last_update'])
    return collection
