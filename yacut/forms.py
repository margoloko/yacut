from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class UrlForm(FlaskForm):
    original_link = URLField('Введите URL',
                             validators=[
                                    DataRequired('Обязательное поле'),
                                    URL(require_tld=True,
                                        message='Некорректная ссылка')])
    custom_id = StringField('Ваш вариант ссылки',
                            validators=[Length(1, 16),
                                        Optional(),
                                        Regexp(r'^[A-Za-z0-9]+$',
                        message='Вы ввели недопустимые символы')])
    submit = SubmitField('Создать')
