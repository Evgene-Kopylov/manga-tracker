import json
import unittest

from fastapi.testclient import TestClient

from db.models import Page
from db.session import SessionLocal

from main import app

session = SessionLocal()

client = TestClient(app)


class TestPage(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'https://www.pytest.pytest/'
        pages = session.query(Page).filter_by(url=self.url)
        for page in pages:
            session.delete(page)
            session.commit()

    def tearDown(self) -> None:
        pages = session.query(Page).filter_by(url=self.url)
        for page in pages:
            session.delete(page)
            session.commit()

    def test_post_page(self):
        response = client.post(
            url="/page",
            headers={
                'api-key': 'api_key2131321554',
            },
            json={
                "url": self.url,
                "element": 'body',
                "block": 'div',
            }
        )
        api_key = json.loads(response.content.decode('utf-8')).get('api-key')
        page = session.query(Page).filter_by(url=self.url).first()
        assert page.url == self.url
        assert api_key

    def test_add_page(self):
        pages = session.query(Page).filter_by(url=self.url).all()
        assert len(pages) == 0
        response = self.request_add_page()
        print(response.url)
        pages = session.query(Page).filter_by(url=self.url).all()
        assert len(pages) == 1

    def request_add_page(self):
        response = client.get(
            url='/add_page',
            params={
                "url": self.url,
                "element": 'body',
                "block": 'div',
            }
        )
        return response

    def test_duplicate_add_page(self):
        pages = session.query(Page).filter_by(url=self.url).all()
        assert len(pages) == 0
        response = self.request_add_page()
        pages = session.query(Page).filter_by(url=self.url).all()
        assert len(pages) == 1
        response = self.request_add_page()
        print(response.url)
        pages = session.query(Page).filter_by(url=self.url).all()
        assert len(pages) == 1

