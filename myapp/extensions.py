from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

"""
    This file is to prevent circular importation.
    
"""

mail_extension = Mail()

jwt = JWTManager()

db = SQLAlchemy()