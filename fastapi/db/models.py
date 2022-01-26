from db.base import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String


class Page(Base):
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    element = Column(String)
    block = Column(String)
    data = Column(String)
    content = Column(String)
    last_check = Column(Date)
    last_update = Column(Date)
    chapters = Column(String(50000), default='')
