import unittest
from db.session import SessionLocal
from db.models import User


class TestPostgreDBSession(unittest.TestCase):

    def setUp(self) -> None:
        self.session = SessionLocal()
        self.email = '***abra+0@cadabra.test'
        user = self.session.query(User).filter_by(email=self.email).first()
        if not user:
            self.test_create_user()

    def tearDown(self) -> None:
        user = self.session.query(User).filter_by(email=self.email).first()
        if user:
            self.test_delete_user()

    def test_create_user(self):
        user = self.session.query(User).filter_by(email=self.email).first()
        if not user:
            user = User()
            user.email = self.email
            self.session.add(user)
            self.session.commit()
            assert user in self.session.query(User).all()

    def test_user_exists(self):
        user = self.session.query(User).filter_by(email=self.email).first()
        assert user

    def test_delete_user(self):
        user = self.session.query(User).filter_by(email=self.email).first()
        print(user.id)
        print(user.email)
        self.session.delete(user)
        self.session.commit()

    def test_save_scenario(self):
        pass
