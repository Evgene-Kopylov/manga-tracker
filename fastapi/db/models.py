from db.base import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import backref, relationship

page_user = Table(
    'page_user',
    Base.metadata,
    Column('page_id', Integer, ForeignKey('page.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String)
    password = Column(String)
    pages = relationship(
        'Page',
        secondary=page_user,
        backref=backref('users', lazy='dynamic'))


class Page(Base):
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    element = Column(String)
    block = Column(String)
