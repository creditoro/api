"""
This module is where we setup our Flask app.
"""

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix

import config
from creditoro_api.api import API
from creditoro_api.extensions import AUTH, CORS, DB, LIMITER, MAIL, MIGRATE


def create_app(app_config: config.Base):
    """create_app.

    Args:
        app_config (config.Base): app_config
    """
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.config.from_object(app_config)
    initialize_extensions(app=app)

    return app


def initialize_extensions(app: Flask):
    """initialize_extensions.

    Args:
        app (Flask): app
    """
    DB.init_app(app=app)
    MIGRATE.init_app(app=app, db=DB)
    LIMITER.init_app(app=app)
    CORS.init_app(app=app)
    AUTH.init_app(app=app)
    MAIL.init_app(app=app)
    sentry_sdk.init(integrations=[FlaskIntegration()],
                    release="0.0.1",
                    send_default_pii=True)

    # Flask Rest PLUS
    API.init_app(app=app)
