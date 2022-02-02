from datetime import datetime
from typing import List

from db.base import Base
from sqlalchemy import Column, DateTime, Integer, String, TEXT


def selector_fix(selector):
    while '..' in selector:
        selector = selector.replace("..", ".")
    return selector


class Page(Base):
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    name = Column(String(200), nullable=False, default='no name provided')
    _element = Column(String)

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, selector):
        self._element = selector_fix(selector)

    _block = Column(String)

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, selector):
        self.name = selector_fix(selector)

    block_html = Column(TEXT)
    last_check = Column(DateTime, default=datetime.now())
    last_update = Column(DateTime, default=datetime.now())
    chapters = Column(String(50000), default='')
    new = Column(Integer, default=0)

    def chapters_list(self) -> List:
        """

        :return: List of chapters
        """
        return [x for x in self.chapters.split(', ') if x]

    def chapters_total(self) -> int:
        """

        :return: number of detected chapters
        """
        return len(self.chapters_list())
