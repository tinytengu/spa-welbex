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


def row_to_dict(row):
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())


# CORS
CORS(app)


@app.route('/', methods=['GET'])
def index():
    '''Index page / sanity check'''
    return jsonify('Backend is up')


@app.route('/items/', methods=['GET'])
def get_items():
    '''Get all the table items'''

    # Serialization
    arg_names = ('sort_by', 'sort_type', 'sort_value')
    for k in request.args.to_dict():
        if k not in arg_names:
            return jsonify({'error': f"Invalid argument '{k}'"})

    # Marshaling
    args = {
        name: request.args.get(name) for name in arg_names
    }

    # sort_by argument
    sort_by = args['sort_by']
    if sort_by:
        sort_options = ('name', 'amount', 'distance')
        if sort_by not in sort_options:
            return jsonify({'error': f"Invalid sort_by option: '{sort_by}'"})

    # sort_type argument
    sort_type = args['sort_type']
    if sort_type:
        if not sort_by:
            return jsonify({'error': "'sort_by' argument required"})

        sort_types = ('contains', 'exact', 'bigger', 'lower')
        if sort_type not in sort_types:
            return jsonify({'error': f"Invalid sort_type option: '{sort_type}'"})

    # sort_value argument
    sort_value = args['sort_value']
    if sort_value and not (sort_by and sort_type):
        return jsonify({'error': "Both 'sort_value' and 'sort_type' arguments are required"})
    elif (sort_by and sort_type) and not sort_value:
        return jsonify({'error': "'sort_value' argument required"})

    if sort_type in ('bigger', 'lower') and sort_by == 'name':
        return jsonify({'error': "Invalid sorting type for the 'name' field"})

    # Fetch database items
    items = list(map(row_to_dict, TableItem.query.all()))

    # Sorting
    if sort_by and sort_type and sort_value:
        items = [
            i for i in items
            if sort_type == 'contains' and sort_value in str(i[sort_by]) or
            sort_type == 'exact' and sort_value == str(i[sort_by]) or
            sort_type == 'bigger' and float(i[sort_by]) > float(sort_value) or
            sort_type == 'lower' and float(i[sort_by]) < float(sort_value)
        ]

    # Return items to the client
    return jsonify(items)


@app.route('/items/', methods=['POST'])
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


@app.route('/items/<id>', methods=['PUT'])
def modify_item(id: int):
    '''Modify table item'''

    # Serialization
    fields = ('date', 'name', 'amount', 'distance')
    for k in request.form.to_dict():
        if k not in fields:
            return jsonify({'error': f"Invalid field '{k}'"})

    # Marshaling
    data = {
        field: request.form[field] for field in fields
        if request.form.get(field)
    }

    # Validation
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


@app.route('/items/<id>', methods=['DELETE'])
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
