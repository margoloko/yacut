from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .models import URLMap


class UrlForm(FlaskForm):
    original_link = URLField('Введите URL',
                             validators=[
                                    DataRequired('Обязательное поле'),
                                    ])
    custom_id = URLField('Ваш вариант ссылки',
                            validators=[
                                        Length(1, 16),
                                        Regexp(r'^[A-Za-z0-9]+$',
                        message='Вы ввели недопустимые символы'),
                        Optional()])
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            print(f'Имя {field.data} уже занято!')
