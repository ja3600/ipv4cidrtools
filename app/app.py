#!/usr/bin/python

'''

CIDRTOOLS ver 2.0

 Web app to help with working with IP subnets
 Based on Flask web application framework

 Github: https://github.com/ja3600/cidrtools

'''

from secrets import token_urlsafe


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_urlsafe(32)

    #default subnet
    working_ipv4 = "192.168.10.0"
    working_prefixlen = 24

    from .routes import main
    app.register_blueprint(main)

    return app

