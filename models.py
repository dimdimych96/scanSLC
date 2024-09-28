# app/models.py

from app import db
from datetime import datetime
import json

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    date = db.Column(db.Date, nullable=False)
    packages = db.relationship('Package', backref='event', lazy=True)

    def __repr__(self):
        return f'<Event {self.name}>'

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    items = db.Column(db.Text, nullable=False)  # Сериализованный JSON список товаров
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def get_items(self):
        return json.loads(self.items)

    def __repr__(self):
        return f'<Package {self.name}>'
