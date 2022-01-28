from datetime import datetime

from db.base import Base
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String


class Page(Base):
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    name = Column(String(200))
    element = Column(String)
    block = Column(String)
    data = Column(String)
    content = Column(String)
    last_check = Column(DateTime, default=datetime.now())
    last_update = Column(DateTime, default=datetime.now())
    chapters = Column(String(50000), default='')
