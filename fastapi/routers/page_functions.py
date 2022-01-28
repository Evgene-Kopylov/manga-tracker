
def remove_index_number(s):
    """уберает цифры в начале строки"""
    res = ''
    for char in s:
        if res and char.isdigit():
            res += char
        if not char.isdigit():
            res += char
    return res


def get_name(url):
    split_address = [i for i in url.split('/') if i != '']
    # print(f"{split_address=}")
    reserv = ' '.join(split_address[1:2])
    if len(split_address) <= 2:
        return split_address[-1]
    if len(split_address) > 2:
        path = split_address[2:4]
    for i in range(len(path)):
        spesial_words = ['manga', 'comics']
        if path[i] in spesial_words:
            path[i] = ''
        path[i] = remove_index_number(path[i])
    line = ' '.join(i for i in path)
    if line == '':
        line = reserv
    name = line[0]
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