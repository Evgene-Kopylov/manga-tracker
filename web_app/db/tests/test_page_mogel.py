import time
from datetime import datetime, timedelta

from db.models import Page


def test_add_chapters():
    page = Page()
    page._chapters = 'q, w, e'
    assert page.total == 3
    assert page.new == (0 or None)
    page.new = 0
    page.add_chapters(['a'])
    assert page.total == 4
    page.add_chapters(['q'])
    assert page.total == 4


def test_parsing_attempt():
    page = Page()
    page.parsing_start = datetime.now()
    assert page.pending
    time.sleep(0.05)
    page.parsing_stop = datetime.now()
    print((datetime.now() - page.parsing_start).microseconds)
    assert 50_000 < (datetime.now() - page.parsing_start).microseconds
    assert 100_000 > (datetime.now() - page.parsing_start).microseconds


def test_pending():
    page = Page()
    assert page.pending is False
    page.parsing_start = datetime.now()
    assert page.pending is True
    page.parsing_stop = datetime.now()
    assert page.pending is False
    page.parsing_start = datetime.now() - timedelta(seconds=11)
    assert page.pending is False
