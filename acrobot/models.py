from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Acronym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym_key = db.Column(db.Text, index=True)
    acronym_definition = db.Column(db.Text)
    user_id_created_by = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, key, definition):
        self.acronym_key = key
        self.acronym_definition = definition

    def __repr__(self):
        return '<key {}, value {}>'.format(self.acronym_key, self.acronym_definition)

    @classmethod
    def create(cls, key, definition):
        acronym = cls(key, definition)
        db.session.add(acronym)
        db.session.commit()

        return acronym
