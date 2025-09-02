#!/usr/bin/python

'''

CIDRTOOLS ver 2.0

 Web app to help with working with IP subnets
 Based on Flask web application framework

 Github: https://github.com/ja3600/ipv4cidrtools

'''

from flask import Flask
from secrets import token_urlsafe

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_urlsafe(32)
    #app.config['DEBUG'] = True  # Enable debug mode

    from .routes import main
    app.register_blueprint(main)

    return app