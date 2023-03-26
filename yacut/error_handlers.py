from flask import jsonify, render_template
from http import HTTPStatus as HS

from . import app, db


class InvalidAPIUsage(Exception):
    """Кастомный классов исключений для API."""
    status_code = HS.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Метод для сериализации переданного сообщения об ошибке."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обработчик кастомного исключения для API.
    Возвращает в ответе текст ошибки и статус-код."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), HS.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), HS.INTERNAL_SERVER_ERROR
