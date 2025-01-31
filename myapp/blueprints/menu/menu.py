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
        - This endpoint renders "MenuC.html" with the available products. MenuC also extends a base template.

        ### Template variables
        - `base_template`: The base HTML template to be used as a layout.
        - `data`: A list of tuples containing product information with the following structure:
            - `product_name` (string): The name of the product.
            - `price` (float): The price of the product.
            - `description` (string): A description of the product.
            - `category` (string): The category to which the product belongs.
        
    """
    try:
        data = db.session.execute(db.select(products.product_name, products.price, products.description, products.category).where(products.available == True)).all()
        base_template = 'base.html'
    except Exception as e:
        print(f"Error: {e}")
        return "Internal server error"
    return render_template('menu.html')
