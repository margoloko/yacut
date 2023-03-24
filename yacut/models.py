from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    original = db.Column(db.String,
                         nullable=False)
    short = db.Column(db.String(16),
                      unique=True,
                      nullable=True)
    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short)

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['short_link'])

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            print(f'Имя {field.data} уже занято!')
