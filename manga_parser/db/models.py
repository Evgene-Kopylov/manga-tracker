from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, TEXT

from db.base import Base


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
    parsing_attempt = Column(String)

    @property
    def parsing_start(self) -> datetime:
        t_start = self.parsing_attempt.split('\n')[0] if self.parsing_attempt else ''
        return datetime.strptime(t_start, '%Y-%m-%d %H:%M:%S.%f')

    @parsing_start.setter
    def parsing_start(self, value: datetime):
        self.parsing_attempt = str(value)

    @property
    def parsing_stop(self) -> datetime | None:
        if self.parsing_attempt:
            st = self.parsing_attempt.split('\n')[0]
            return datetime.strptime(st, '%Y-%m-%d %H:%M:%S.%f')

    @parsing_stop.setter
    def parsing_stop(self, value: datetime):
        dif = (value - datetime.strptime(self.parsing_attempt, '%Y-%m-%d %H:%M:%S.%f')).microseconds
        self.parsing_attempt += '\n' + str(value)
        self.parsing_attempt += '\n' + str(dif)

    @property
    def pending(self) -> bool:
        pa = self.parsing_attempt.split('\n') if self.parsing_attempt else []
        if len(pa) != 1:
            return False
        dif = (datetime.now() - datetime.strptime(pa[0], '%Y-%m-%d %H:%M:%S.%f')).seconds
        if dif > 10:
            return False
        return True

    @pending.setter
    def pending(self, val: bool):
        if val:
            self.parsing_start = datetime.now()

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
