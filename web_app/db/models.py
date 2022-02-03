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
    _block = Column(String)
    block_html = Column(TEXT)
    last_check = Column(DateTime, default=datetime.now())
    last_update = Column(DateTime, default=datetime.now())
    _chapters = Column(String(50000), default='')
    new = Column(Integer, default=0)

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, selector):
        self._element = selector_fix(selector)

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, selector):
        self._block = selector_fix(selector)

    @property
    def chapters(self) -> List:
        if self._chapters:
            return [x for x in self._chapters.split(', ') if x]
        else:
            return []

    @chapters.setter
    def chapters(self, chapters: List):
        self._chapters = ', '.join(chapters)

    def add_chapters(self, chapters: List):
        """add new unique chapters"""
        n = self.total
        self.chapters += [c for c in chapters if c not in self.chapters]
        self.new += self.total - n

    @property
    def total(self):
        return len(self.chapters)
