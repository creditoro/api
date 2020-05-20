import os
import uuid


class Base:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", str(uuid.uuid4()))
    POSTGRES = {
        "user": os.environ["POSTGRES_USER"],
        "pw": os.environ["POSTGRES_PASSWORD"],
        "db": os.environ["POSTGRES_DB"],
        "host": os.environ["POSTGRES_HOST"],
        "port": os.environ["POSTGRES_PORT"],
    }
    SQLALCHEMY_DATABASE_URI = "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    SECURITY_PASSWORD_SALT = "bald-manc"


class DevelopmentConfig(Base):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = False


class TestingConfig(Base):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = True


class ProductionConfig(Base):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


CONFIG_DICT = {
    "PRODUCTION": ProductionConfig(),
    "TEST": TestingConfig(),
    "DEV": DevelopmentConfig()
}
