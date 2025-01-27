from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager

"""
    This file is used to prevent circular importation.
    
"""

class Base(DeclarativeBase):
    pass

mail_extension = Mail()

jwt = JWTManager()

db = SQLAlchemy(model_class=Base)