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
    if '?' in name:
        name = name[:name.index('?')]
    name = name.replace('-', ' ')
    name = name.replace('  ', ' ')
    name = name.strip()

    return name[:100]
