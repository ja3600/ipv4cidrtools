from flask import Flask
from secrets import token_urlsafe

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_urlsafe(32)

    from .routes import main
    app.register_blueprint(main)

    return app