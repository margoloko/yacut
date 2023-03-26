import random
import string

from .models import URLMap


def get_unique_short_id():
    """Функция формирования коротких идентификаторов переменной длины."""
    chars = string.ascii_letters + string.digits
    length = 6
    short_id = ''.join(random.choice(chars) for _ in range(length))
    urlmap = URLMap.query.filter_by(id=short_id).first()
    while urlmap:
        short_id = ''.join(random.choice(chars) for _ in range(length))
        urlmap = URLMap.query.filter_by(short=short_id).first()
    return short_id


def check_unique_short_url(custom_id):
    """Проверка уникальности значения короткой ссылки."""
    if URLMap.query.filter_by(short=custom_id).first():
        return custom_id
    return None
