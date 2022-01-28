from routers.page_utilitys import remove_index_number, get_name


def test_get_name():
    url = "https://mangabuddy.com/i-am-the-fated-villain"
    assert get_name(url) == "I Am The Fated Villain"


def test_remove_index_number():
    line = '123qwer123'
    assert remove_index_number(line) == 'qwer123'
