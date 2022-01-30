from routers.page_utils import remove_index_number, get_name


def test_get_name():
    url = "https://mangabuddy.com/i-am-the-fated-villain"
    assert get_name(url) == "I Am The Fated Villain"
    url = "https://mangasee123.com/manga/Murim-Login#unavailable"
    assert get_name(url) == "Murim Login"

def test_remove_index_number():
    line = '123qwer123'
    assert remove_index_number(line) == 'qwer123'
