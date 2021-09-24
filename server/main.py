import os
from datetime import datetime
from dataclasses import dataclass

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Dotenv
load_dotenv()

# Flask Application
app = Flask(__name__)
app.url_map.strict_slashes = False

# SQLAlchemy
app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4' % (
        os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOSTNAME"), os.getenv("DB_DATABASE")
    ),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})
db = SQLAlchemy(app)


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


# CORS
CORS(app)


@app.route('/', methods=['GET'])
def index():
    '''Index page / sanity check'''
    return jsonify('Backend is up')


@app.route('/data/', methods=['GET'])
def get_items():
    '''Get all the table items'''
    items = TableItem.query.all()
    return jsonify(items)


@app.route('/data/', methods=['POST'])
def add_item():
    '''Add new table item'''

    # Serialization (don't want to write my own or use flask-restful, sorry)
    fields = ('date', 'name', 'amount', 'distance')
    data = {
        field: request.form.get(field) for field in fields
    }

    # Fields validation
    for k, v in data.items():
        if v is None:
            return jsonify({'error': f"'{k}' field cannot be empty"})

    # Add new item to the database
    item = TableItem(**data)
    db.session.add(item)
    db.session.commit()

    # Return result to the client
    return jsonify(item)


@app.route('/data/<id>', methods=['PUT'])
def modify_item(id: int):
    '''Modify table item'''

    # Serialization
    fields = ('date', 'name', 'amount', 'distance')
    for k in request.form.to_dict():
        if k not in fields:
            return jsonify({'error': f"Invalid field '{k}'"})

    # Fields validation
    data = {
        field: request.form[field] for field in fields
        if request.form.get(field)
    }

    if not data:
        return jsonify({'error': 'Data cannot be empty'})

    # Fetching item
    item = TableItem.query.get(id)
    if item is None:
        return jsonify({'error': f"Invalid item id: {id}"})

    # Update item values
    for k, v in data.items():
        item.__setattr__(k, v)
    db.session.commit()

    # Return new item to the client
    return jsonify(item)


@app.route('/data/<id>', methods=['DELETE'])
def delete_item(id: int):
    '''Delete table item'''

    # Fetching item
    item = TableItem.query.get(id)
    if item is None:
        return jsonify({'error': f"Invalid item id: {id}"})

    # Delete item
    db.session.delete(item)
    db.session.commit()

    # Return deleted item to the client
    return jsonify(item)


if __name__ == '__main__':
    db.create_all()
    db.session.commit()

    app.run(host='127.0.0.1', port=5000, debug=True)
