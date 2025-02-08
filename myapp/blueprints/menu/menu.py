from flask import Blueprint, redirect, render_template, url_for
from myapp import db, products

bp_menu = Blueprint("bp_menu", __name__, template_folder="templates", static_folder="static", static_url_path="/menu/static")


@bp_menu.route("/")
def idle():
    """
        Redirects the user to the main page.
    """
    return redirect(url_for("bp_menu.menu"))

@bp_menu.route("/menu", methods=["GET"])
def menu():
    """
        Returns a template of the menu.

        ### Endpoint
        - Method: GET
        - URL: /Menu 

        ### Template
        - This endpoint renders "menu.html" with the available products. M
    """
    return render_template('menu.html')


