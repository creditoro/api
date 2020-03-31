#!/usr/bin/python3
import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix

import config
from src.api import API
from src.extensions import DB, MIGRATE, LIMITER, CORS, MAIL


def create_app(app_config: config.Base):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.config.from_object(app_config)
    initialize_extensions(app=app)

    return app


def initialize_extensions(app: Flask):
    DB.init_app(app=app)
    MIGRATE.init_app(app=app, db=DB)
    LIMITER.init_app(app=app)
    CORS.init_app(app=app)
    MAIL.init_app(app=app)
    sentry_sdk.init(
        integrations=[FlaskIntegration()],
        release="0.0.1",
        send_default_pii=True
    )

    # Flask Rest PLUS
    API.init_app(app=app)
