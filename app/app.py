from flask import Flask
from database import db
from api import api


def create_app():
    """Creates app, configure database and register blueprint"""
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:football@db/football_league'
    db.init_app(app)
    app.register_blueprint(api, url_prefix='')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=9090, threaded=False, debug=True)
