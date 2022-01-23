import unittest

from db.models import Page
from db.session import SessionLocal


class TestPostgresDBSession(unittest.TestCase):

    def setUp(self) -> None:
        self.session = SessionLocal()
        self.url = 'http://abra.cadabra.test'
        pages = self.session.query(Page).filter_by(url=self.url)
        if not pages:
            self.test_create_page()

    def tearDown(self) -> None:
        pages = self.session.query(Page).filter_by(url=self.url).all()
        if pages:
            for _ in pages:
                self.test_delete_page()

    def test_create_page(self):
        page = self.session.query(Page).filter_by(url=self.url).first()
        if not page:
            page = Page()
            page.url = self.url
            self.session.add(page)
            self.session.commit()
            assert page in self.session.query(Page).all()

    def test_delete_page(self):
        page = self.session.query(Page).filter_by(url=self.url).first()
        if not page:
            self.test_create_page()
        page = self.session.query(Page).filter_by(url=self.url).first()
        self.session.delete(page)
        self.session.commit()
