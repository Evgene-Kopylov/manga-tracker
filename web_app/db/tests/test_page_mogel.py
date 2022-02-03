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
