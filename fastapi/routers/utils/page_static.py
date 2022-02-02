

def cut_selector(selector):
    while '..' in selector:
        selector = selector.replace("..", ".")
    return selector


