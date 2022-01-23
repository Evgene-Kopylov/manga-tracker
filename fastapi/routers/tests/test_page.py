import json

from fastapi.testclient import TestClient

from db.models import Page
from db.session import SessionLocal

from main import app

session = SessionLocal()

client = TestClient(app)


class TestPage:
    def test_add_page(self):
        response = client.post(
            url="/page",
            headers={
                'api-key': 'api_key2131321554',
            },
            json={
                "url": 'https://www.jetbrains.com/',
                "element": 'body',
                "block": 'div',
            }
        )
        api_key = json.loads(response.content.decode('utf-8')).get('api-key')
        page = session.query(Page).filter_by(url='https://www.jetbrains.com/').first()
        assert page.url == 'https://www.jetbrains.com/'
        assert api_key
