from fastapi.testclient import TestClient
from db.session import SessionLocal
from main import app


session = SessionLocal()

client = TestClient(app)


class TestAny:
    """
    playground
    """
    def test_get(self):
        response = client.get(url="/")
        print(response.content.decode('utf-8'))
