import os

from flask import Flask, jsonify
from flask_cors import CORS

from .db import db
from .items import bp as items_bp


# Flask Application
app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS
CORS(app)


@app.route('/', methods=['GET'])
def index():
    '''Index page / sanity check'''
    return jsonify('Backend is up')


def init_app():
    # Endpoints
    app.register_blueprint(items_bp)

    # SQLAlchemy
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4' % (
            os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOSTNAME"), os.getenv("DB_DATABASE")
        ),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()
        db.session.commit()

    return app
