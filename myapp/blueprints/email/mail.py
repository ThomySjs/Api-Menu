from flask import Blueprint, request, jsonify, render_template
from myapp import db, users, mail_extension
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import os
from flask_mail import Message, sanitize_address
from email_validator import validate_email, EmailNotValidError
from smtplib import SMTPException

bp_mail = Blueprint("bp_mail", __name__, template_folder="templates", static_folder="static")

def send_email(mail):
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
        token = serializer.dumps(mail, salt=os.getenv("SECURITY_SALT"))
        route = request.url_root + "mail/validate/%s" % token
        msg = Message(
            'Email verification',
            recipients=[mail],
            html= render_template('template.html', route = route, request = request),
            sender=os.getenv('MAIL_DEFAULT_SENDER')
        )
        mail_extension.send(msg)
    
@bp_mail.route("/send-mail", methods=["POST"])
def resend_email():
    """
        Sends a confirmation link to the given email.

        ### Endpoint
        - Method: POST
        - URL: /send-mail
        - Content-type: JSON

        ### Payload example:

        {"mail": example@gmail.com}

        ### Template
        - This endpoint uses a template for the email.

        ### Template variables
        - `key`: adds the token to the confirmation link.

        ### Responses:
        - Content-type JSON

        - 200 Sent

            {"message": "Email sent"}

        - 400 Bad request

            {"error" : "Request method must be JSON type"}
            {"error": "Missing data.", "keys": "mail"}
            {"error": "Email is already verified."}

        - 404 Not registered 

            {"error": "The email is not registered."}

        - 500 Internal error

            {"error": "Failed to send the email."} SMTP Exception
            {"error": "An internal error occurred. Please try again later."}, 500


        ### Notes:
        - Validates the email and sanitizes it, raises an exception if the email is invalid.
        - URLSafeTimedSerializer is used to create a validation token with the application`s secret key.
        - Token is salted by a security salt declared on the environment variables.
        
    """
    if not request.is_json:
        return jsonify({"error" : "Request method must be JSON type"}), 400
    
    data = request.get_json()

    if "mail" not in data:
        return jsonify({"error": "Missing data.", "keys": "mail"}), 400
    
    try:
        validate_email(data["mail"])
    except EmailNotValidError:
        return jsonify({"error": "Invalid email"}), 400
    
    mail = sanitize_address(data["mail"]).lower()

    verification_data = db.session.execute(db.select(users.email, users.verified).filter_by(email=mail)).first()

    if verification_data is None:
        return jsonify({"error": "The email is not registered."}), 404
    
    #Checks if the email is already verified.
    if verification_data[1]:
        return jsonify({"error": "Email is already verified."}), 400
    try:
        send_email(mail)
        return jsonify({"message": "Email sent"}), 200
    except SMTPException as e:
        print(f"SMTP error: {(e)}")
        return jsonify({"error": "Failed to send the email."}), 500
    except Exception as e:
        print(f"An error ocurred: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500


@bp_mail.route("/validate/<token>", methods=["GET"])
def validate_token(token):
    """
        Verifies the email.

        ### Endpoint
        - Method: GET
        - URL: /validate/<token>

        ### Responses:
        - Content-type JSON

        - 200 Ok

            {"message": "Email verified."}

        - 400 Bad request

            {"error": "The token is no longer available."}
            {"error": "Verification failed.", "details": "Wrong token."}
            {"error": "The email is already verified."}


        - 500 Internal error

            {"error": "An internal error occurred. Please try again later."}, 500


        ### Notes:
        - The token is set to last for 180 seconds.        
    """
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        mail = serializer.loads(token, salt=os.getenv("SECURITY_SALT"), max_age=180)

        verified = db.session.execute(db.select(users.verified).filter_by(email=mail.lower())).first()

        #Checks if the email is verified.
        if verified[0]:
            return jsonify({"error": "The email is already verified."}), 400

        db.session.execute(db.update(users).where(users.email == mail).values(verified = True))
        db.session.commit()
        return jsonify({"message": "Email verified."}), 200
    except BadSignature:
        return jsonify({"error": "Verification failed.", "details": "Wrong token."}), 400
    except SignatureExpired :
        return jsonify({"error": "The token is no longer available."}), 400
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500
    