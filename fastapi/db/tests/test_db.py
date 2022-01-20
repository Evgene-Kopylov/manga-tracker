import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.session import SessionLocal
from db.models import User


class TestPostgreDB(unittest.TestCase):

    def setUp(self) -> None:
        self.db = SessionLocal()
        self.email = 'abra+0@cadabra.test'

    def tearDown(self) -> None:
        pass

    def test_create_user(self):
        user = self.db.query(User).filter_by(email=self.email).first()
        if not user:
            user = User()
            user.email = self.email + '123'
            self.db.add(user)
            self.db.commit()
            assert user in self.db.query(User).all()

    # def test_user_exists(self):
    #     user = self.db.query(User).filter_by(email=self.email).first()
    #     assert user

    # def test_delete_user(self):
    #     user = self.db.query(User).filter_by(email=self.email).first()
    #     print(user.id)
    #     user = User.query.get(1)
    #     print(user.id)
        #
        # self.db.delete(user)
        # self.db.commit()
        # user = self.db.query(User).filter_by(email=self.email).first()
        # assert not user

    def test_save_scenario(self):
        pass
