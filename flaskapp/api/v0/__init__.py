from flask import Flask
from api.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # this is used to allow for future expansion oof the database

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    from .errors import app_err
    app.register_blueprint(app_err)

    from .user import user_app
    app.register_blueprint(user_app, url_prefix='/api/v0/user')
    # app.register_blueprint(auth_bp, url_prefix='/auth')  # this include /auth in url

    return app


from .user.models import user_model
