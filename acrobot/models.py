from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Acronym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym_key = db.Column(db.Text, index=True)
    acronym_definition = db.Column(db.Text)
    user_created_by = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, key, definition, created_by=None):
        self.acronym_key = key
        self.acronym_definition = definition
        self.user_created_by = created_by or "N/A"

    def __repr__(self):
        return '<key {}, value {}>'.format(self.acronym_key, self.acronym_definition)

    @classmethod
    def create(cls, key, definition, created_by=None):
        # To make sql queries easier, enforce all keys to be lowercase
        acronym = cls(key.lower(), definition, created_by=created_by)
        db.session.add(acronym)
        db.session.commit()

        return acronym


# Model helper, probably belongs in utils submodule
def find_acronyms(search_key):
    return Acronym.query.filter_by(acronym_key=search_key.lower()).all()
