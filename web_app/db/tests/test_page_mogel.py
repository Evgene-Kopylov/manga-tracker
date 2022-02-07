import time
from datetime import datetime

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
    assert page.processing
    time.sleep(0.05)
    page.parsing_stop = datetime.now()
    print((datetime.now() - page.parsing_start).microseconds)
    assert 50_000 < (datetime.now() - page.parsing_start).microseconds
    assert 100_000 > (datetime.now() - page.parsing_start).microseconds
