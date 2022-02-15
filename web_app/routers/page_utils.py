from datetime import datetime
from typing import List

from db.models import Page
from db.session import SessionLocal

session = SessionLocal()


def get_pages() -> List:
    pages = session.query(Page).all()
    pages.sort(key=lambda x: (datetime.now() - x.last_update).seconds)
    print([(datetime.now() - x.last_update).seconds for x in pages])
    collection = [
        {
            'id': page.id,
            'url': page.url,
            'name': page.name,
            'last_chapters': page.chapters[:5],
            'total': page.total,
            'last_check': str(page.last_check),
            'last_update': str(page.last_update),
            'new': page.new,
            'pending': page.pending
        } for page in pages
    ]
    return collection


def remove_index_number(line: str) -> str:
    """
    Remove trailing digits at start of string

    :param line: part of url
    :return:
    """
    res = ''
    for char in line:
        if res:
            res += char
        elif not char.isdigit():
            res += char
    return res


def get_name(url: str) -> str:
    """
    Extracts name from url

    :param url: page.url
    :return: convenient part of page.url
    """
    if '#' in url:
        url = url[:url.index('#')]
    if '?' in url:
        url = url[:url.index('?')]

    split_address = [i for i in url.split('/') if i != '']
    # print(f"{split_address=}")
    reserve = ' '.join(split_address[1:2])
    if len(split_address) <= 2:
        return split_address[-1]
    path = split_address[2:4]
    for i in range(len(path)):
        special_words = ['manga', 'comics']
        if path[i] in special_words:
            path[i] = ''
        path[i] = remove_index_number(path[i])
    line = ' '.join(i for i in path)
    if line == '':
        line = reserve
    name = line[0].upper()
    for i in range(1, len(line)):
        if not line[i - 1].isalpha() and line[i].isalpha():
            name += line[i].upper()
        else:
            name += line[i]
    name = name.replace('-', ' ')
    name = name.replace('  ', ' ')
    name = name.strip()

    return name[:100]
