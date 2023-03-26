from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import UrlForm
from .models import URLMap
from .utils import get_unique_short_id, check_unique_short_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция главной страницы."""
    form = UrlForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short is None or not short or len(short) == 0:
            short = get_unique_short_id()
        if check_unique_short_url(short):
            flash(f'Имя {short} уже занято!', "error")
            return render_template('index.html', form=form)
        url_map = URLMap(original=form.original_link.data,
                         short=short)
        db.session.add(url_map)
        db.session.commit()
        flash(url_for('redirect_url', short=short, _external=True), "redirect")
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    """Функция, отвечающая за переадресацию.."""
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
