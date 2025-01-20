from flask import Flask
from .extensions import db, mail_extension, jwt
from dotenv import load_dotenv, find_dotenv
from .models import *
from .blueprints.validation.auth import auth_bp
from .blueprints.email.mail import bp_mail
from .blueprints.menu.menu import bp_menu
from .blueprints.product.products import bp_product

import os

def create_app():
    app = Flask(__name__)
    load_dotenv(find_dotenv())

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['SECURITY_SALT'] = os.getenv('SECURITY_SALT')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    app.config['JSON_AS_ASCII'] = False

    app.register_blueprint(auth_bp)
    app.register_blueprint(bp_mail)
    app.register_blueprint(bp_menu)
    app.register_blueprint(bp_product)

    mail_extension.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app
