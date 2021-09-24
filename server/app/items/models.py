from datetime import datetime
from dataclasses import dataclass

from ..db import db


@dataclass
class TableItem(db.Model):
    __tablename__ = 'items'

    # Serialization fields
    id: int
    date: datetime
    name: str
    amount: int
    distance: float

    # Model fields
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)
