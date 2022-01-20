from werkzeug.security import generate_password_hash, check_password_hash


def test_hash():
    password = "123456"
    my_hash = generate_password_hash(password, method='sha256')
    assert password != my_hash
    assert check_password_hash(my_hash, password)
