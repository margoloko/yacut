from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class UrlForm(FlaskForm):
    """Форма для создания короткой ссылки."""
    original_link = URLField('Введите URL',
                             validators=[DataRequired('Обязательное поле'),
                                         ])
    custom_id = StringField('Ваш вариант ссылки',
                            validators=[Length(1, 16),
                                        Regexp(r'^[A-Za-z0-9]+$',
                                        message='Вы ввели недопустимые символы'),
                                        Optional()])
    submit = SubmitField('Создать')
