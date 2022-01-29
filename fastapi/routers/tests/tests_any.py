import unittest

from fastapi.testclient import TestClient
from db.session import SessionLocal
from main import app, get_pages

session = SessionLocal()

client = TestClient(app)


class TestAny(unittest.TestCase):
    """
    playground
    """

    def test_get(self):
        response = client.get(url="/")
        print(response.content.decode('utf-8'))

    def test_post(self):
        msg = {'msg': 'OK'}
        response = client.post(
            url='/abr',
            headers={'api-key': 'api_key2131321554',
                     'api-secret': 'api_secret',
                     'agent-id': 'agent_id'},
            json={'msg1': 'OK'})
        print('')
        print(response.content.decode('utf-8'))

    def test_get_pages(self):
        print(get_pages())

