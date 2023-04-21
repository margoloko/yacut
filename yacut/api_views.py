from flask import jsonify, request
from re import match
from http import HTTPStatus as HS

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .view import get_unique_short_id


ALLOWED_CHECK_ID = '^[a-zA-Z0-9_]*$'
LENGTH_CUSTOM_ID = 16


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    """Получить оригинальную ссылку по короткой ссылке.

    :param short_id: короткая ссылка
    :return: словарь с оригинальной ссылкой
    :rtype: dict
    """
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HS.NOT_FOUND)
    return jsonify({'url': url.original}), HS.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    """
    Добавить новую короткую ссылку.

    :return: словарь с добавленной короткой ссылкой
    :rtype: dict
    """
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get('custom_id')
    if 'custom_id' not in data or custom_id is None:
        data['custom_id'] = get_unique_short_id()
    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
        if not match(ALLOWED_CHECK_ID, custom_id) or len(custom_id) > LENGTH_CUSTOM_ID:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HS.CREATED
