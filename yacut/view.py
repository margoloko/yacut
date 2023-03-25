
import random
import string
from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short is None:
            short = get_unique_short_id()
        if check_unique_short_url(short):
            flash(f'Имя {short} уже занято!')
        url_map = URLMap(original=form.original_link.data,
                         short=short)
        db.session.add(url_map)
        db.session.commit()
        flash(url_for('redirect_url', short=short, _external=True))
    return render_template('index.html', form=form)


def get_unique_short_id():
    chars = string.ascii_letters + string.digits
    length = 6
    short_id = ''.join(random.choice(chars) for _ in range(length))
    urlmap = URLMap.query.filter_by(id=short_id).first()
    while urlmap:
        short_id = ''.join(random.choice(chars) for _ in range(length))
        urlmap = URLMap.query.filter_by(short=short_id).first()
    return short_id


def check_unique_short_url(custom_id):
    if URLMap.query.filter_by(short=custom_id).first():
        return custom_id
    return None


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
