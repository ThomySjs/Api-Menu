from flask import Blueprint, request, jsonify
from myapp.models import users
from myapp import db, jwt
import os
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_mail import sanitize_address
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from ..email.mail import send_email
from smtplib import SMTPException

auth_bp = Blueprint('auth_bp', __name__)

@jwt.user_identity_loader
def user_loader(user):
    return json.dumps(user)

@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
        Register endpoint that works with a pre-made secret key. 

        ### Endpoint
        - Method: POST
        - URL: /register
        - Content-type: JSON

        ### Payload:
            {
                name: "yourname",
                mail: "example@gmail.com",
                password: "supersecretpassword",
                key: "supersecretkey"
            }

        ### Response examples:
        - Content-type: JSON

        - 201 Created

            {"message": "Account succesfully created!"}

        - 400 Bad request

            {"error": "Request must be JSON type."}
            {"error": "Incorrect registration key."}
            {"error" : "Missing data. Required fields: name, mail, password, key"}

        - 500 Internal error

            {"error" : "An error ocurred while creating the account."}

        ### Notes:
        - The secret key must be stored as a environment variable.
        - Passwords are securely hashed, plain-text is never stored.

    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON type."}), 400
    
    data = request.get_json()

    required_keys = {"name", "mail", "password", "key"}
    if not required_keys.issubset(data):
        return jsonify({"error" : "Missing data. Required fields: name, mail, password, key"}), 400
    
    mail = data["mail"]
    
    #Checks if the email is valid
    try:
        validate_email(mail)
    except EmailNotValidError:
        return jsonify({"error": "Invalid email"}), 400
    
    mail = sanitize_address(mail).lower()
    
    #Checks the key
    if data["key"] != os.getenv("REGISTRATION_KEY"):
        return jsonify({"error": "Incorrect registration key."}), 400
    
    #Adds the user 
    try:
        hashed_password_str = users.hash_password(data["password"])
        user = users(user_name=data["name"], email=mail, password=hashed_password_str)
        db.session.add(user)
        db.session.commit()
        send_email(mail)
        return jsonify({"message": "Account succesfully created!"}), 201
    except Exception as e:
        db.session.rollback()
        if "UNIQUE constraint failed" in str(e):
            return jsonify({"error": "The email already exists."}), 400
        else:
            print(f"Error: {e}")
            return jsonify({"error" : "An error ocurred while creating the account."}), 500
        

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Log in system with mail and password validation.
    This endpoint validates user credentials and returns a JWT access token if successful.

    - Method: POST
    - URL: /login
    - Content-type: JSON

    ### Payload example:
        {
            mail: "example@gmail.com",
            password: "supersecretpassword"
        }

    ### Responses:
    - Content-type: JSON

    - 200 Ok 

        {access_token: "JWT"}

    - 400 Bad request:

        {"error": "Request type must be JSON type."}
        {"error": "Wrong password."}
        {"error": "Missing data.", "Required data": "mail, password"}
        {"error": "Account is not verified."}

    - 404 Not found

        {"error": "The email is not registered."}

    ### Notes:
    - The JWT (access_token) contains the users name and id.
    - Passwords are securely hashed.
    """

    if not request.is_json:
        return jsonify({"error": "Request type must be JSON type."}), 400
    
    data = request.get_json()
    
    required_keys = {"mail", "password"}
    if not required_keys.issubset(data):
        return jsonify({"error": "Missing data.", "Required data": "mail, password"}), 400
    

    try:
        #Validates the address
        mail = sanitize_address(validate_email(data["mail"].lower()).normalized)

        #Checks if the email is registered. 
        verification_data = db.session.query(users).filter_by(email=mail).first()
        if verification_data is None:
            return jsonify({"error": "The email is not registered."}), 404
        hashed_password = verification_data.password
        verified = verification_data.verified

        #Compares the password against the hashed password.
        if not users.check_password(data["password"], hashed_password):
            return jsonify({"error": "Wrong password."}), 400
        
        #Checks if the email is verified.
        if not verified:
            try:
                send_email(mail)
                return jsonify({"error": "Account is not verified. Check your email"}), 401
            except SMTPException as e:
                print(f"SMTP error: {(e)}")
                return jsonify({"error": "Failed to send the email."}), 500
            except Exception as e:
                print(f"An error ocurred: {e}")
                return jsonify({"error": "An internal error occurred. Please try again later."}), 500
        
        identity= {"id": verification_data.user_id, "name": verification_data.user_name}
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    except EmailNotValidError:
        return jsonify({"error": "Invalid email"}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error, try again."}), 500
    
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
        Returns a new acces token and refresh token using a previous refresh token.

        ### Endpoint
        - Method: POST
        - URL: /refresh

        ### Authorization:
        - This endpoint uses JWT for authorization.

    """
    identity = json.loads(get_jwt_identity())
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return jsonify(access_token = access_token, refresh_token=refresh_token), 200
    

    








    