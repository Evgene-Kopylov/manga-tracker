from fastapi.testclient import TestClient

from db.models import User
from db.session import SessionLocal

from main import app

session = SessionLocal()

client = TestClient(app)


class TestUser:
    def test_user_registration(self):
        email = "qqq@sss.test"
        user = session.query(User).filter_by(email=email).first()
        if user:
            session.delete(user)
            session.commit()

        response = client.post(
            url="/user_registration",
            json={
                "email": email,
                "password": "12312312311dddd"
            }
        )
        user = session.query(User).filter_by(email=email).first()
        assert user
