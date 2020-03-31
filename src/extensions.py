"""
This module is for declaring our extensions. Other modules can then import them from here.
"""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail

from src.cors import Cors

DB = SQLAlchemy()
MIGRATE = Migrate()
LIMITER = Limiter(key_func=get_remote_address, default_limits=["200/minute"])
CORS = Cors()
MAIL = Mail()
