from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from myapp import db, products, change_logg
import json

bp_product = Blueprint("bp_product", __name__)

@bp_product.route("/products", methods=["POST"])
@jwt_required()
def get_products():
    """
        Returns a JSON object containing a list of products sorted by the given key. This endpoint is protected by JWT validation.

        ### Endpoint
        - Method: POST
        - URL: /products
        - Content-type: JSON

        ### Authorization
        - This endpoint is protected by JWT valiadtion.
        
        ### Header example:
            {"Authorization": "Bearer {JWT-HERE}"}

        
        ### Payload example:
            {"order": "price"}

        
        ### Responses: 
        - Content-type: JSON

        - 200 Ok

            "products": [
                {
                    "product_id": 0,
                    "product_name": "productname",
                    "price": 1500.0,
                    "description": "somedescription",
                    "category": "somecategory",
                    "available": True

                }
            ]
    
        - 400 Bad request

            {"error": "Request must be JSON type."}
            {"error": "Missing key", "details": "order"}
            {"error": "Value not supported.", "Supported_values": ["product_id", "product_name", "price", "description", "category", "available"]}

        - 500 Internal error

            {"error": "An internal error occurred. Please try again later."}

    """

    if not request.is_json:
        return jsonify({"error": "Request must be JSON type."}), 400

    order = request.get_json()

    if "order" not in order:
        return jsonify({"error": "Missing key", "details": "order"}), 400

    try: 
        #Returns the atribute of the table
        product_order = getattr(products, order["order"], None)
        if product_order is None:
            return jsonify({"error": "Value not supported.", "Supported_values": ["product_id", "product_name", "price", "description", "category", "available"]}), 400

        prod = db.session.query(products).order_by(product_order).all()

        product_list = [product.toDict() for product in prod]
        return jsonify({"products": product_list}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500


@bp_product.route("/products/add", methods=["POST"])
@jwt_required()
def add_product():
    """
        Adds products to the menu. This endpoint is protected by JWT validation.

        ### Endpoint
        - Method: POST
        - URL: /products/add
        - Content-type: JSON

        ### Authorization
        - This endpoint is protected by JWT valiadtion.
        
        ### Header example:
            {"Authorization": "Bearer {JWT-HERE}"}

        ### Payload example:
            {
                "product_name": "productname",
                "price": 1500.0,
                "description": "somedescription",
                "category": "somecategory",
                "available": False 
            }

        ### Responses:
        Content-type: JSON

        - 200 Added

            {"message": "Product added!"}

        - 400 Bad request

            {"error": "Request must be JSON type."}
            {"error": "Missing keys.", "Required_keys": f"{required_keys}"}

        - 500 Internal error

            {"error": "An internal error occurred. Please try again later."}

        ### Note
        - This endpoint also adds a change log when a product is created.
    """

    if not request.is_json:
        return jsonify({"error": "Request must be JSON type."}), 400
    
    data = request.get_json()

    required_keys = {"product_name", "price", "description", "category", "available"}
    if not required_keys.issubset(data):
        return jsonify({"error": "Missing keys.", "Required_keys": f"{required_keys}"}), 400
    
    try:
        user = json.loads(get_jwt_identity())
        product = products(product_name=data["product_name"], price=data["price"], description=data["description"], category=data["category"], available=data["available"])
        log = change_logg(user_id = user["id"], log=f"{user["name"]} added a product:  {data["product_name"]}")
        db.session.add(product)
        db.session.add(log)
        db.session.commit()

        return jsonify({"message": "Product added!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500
    
@bp_product.route("/products/update", methods=["PUT"])
@jwt_required()
def update_product():
    """
        Updates the given product if exists.

        ### Endpoint
        - Method: PUT
        - URL: /products/update
        - Content-type: JSON

        ### Authorization
        - This endpoint is protected by JWT valiadtion.

        ### Header example:
            {"Authorization": "Bearer {JWT-HERE}"}

        ### Payload example:
            {
                "product_id": 0,
                "product_name": "newname",
                "price": 2000.0,
                "description": "newdescription",
                "category": "newcategory",
                "available": True
            }

        ### Responses:
        Content-type: JSON

        - 200 Updated

            {"message": "Product updated!"}

        - 400 Bad request

            {"error": "Missing keys.", "Required_keys": f"{required_keys}"}

        - 404 Not found

            {"error": "The product doesnt exists."} 

        - 500 Internal error

            {"error": "An internal error occurred. Please try again later."}

        ### Note
        - This endpoint adds a change log when a product is modified.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON type."}), 400
    
    data = request.get_json()

    required_keys = {"product_id", "product_name", "price", "description", "category", "available"}
    if not required_keys.issubset(data):
        return jsonify({"error": "Missing keys.", "Required_keys": f"{required_keys}"}), 400
    
    try:
        user = json.loads(get_jwt_identity())
        result= db.session.execute(db.update(products).where(products.product_id == data["product_id"]).values(product_name=data["product_name"], description=data["description"], price=data["price"], available=data["available"], category=data["category"]))
        if not result.rowcount:
            return jsonify({"error": "The product doesnt exists."}), 404
        log = change_logg(user_id = user["id"], log=f"{user["name"]} changed a product:  {data["product_name"]}")
        db.session.add(log)
        db.session.commit()
        return jsonify({"message": "Product updated!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500
    

@bp_product.route("/products/delete", methods=["DELETE"])
@jwt_required()
def delete_product():
    """
        Deletes a product with the given ID.
        
        ### Endpoint
        - Method: DELETE
        - URL: /products/delete
        - Content-type: JSON

        ### Authorization
        - This endpoint is protected by JWT validation.

        ### Header example:

            {"Authorization": "Bearer {JWT-HERE}"}

        ### Payload example:

            {"product_id": 0}

        ### Responses:
        Content-type: JSON

        - 200 Deleted
        
            {"message": "Product deleted!"}

        - 400 Bad request

            {"error": "Request must be JSON type."}
            {"error": "Missing key: product_id"}

        - 401 Unathorized access #This happens when JWT expires or is invalid. 

        - 404 Not found

            {"error": "The product doenst exists."}

        - 500 Internal error

            {"error": "An internal error occurred. Please try again later."}

        ### Note
        - This endpoint adds a change log when a product is deleted.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON type."}), 400
    
    data = request.get_json()

    if not "product_id" in data:
        return jsonify({"error": "Missing key: product_id"}), 400
    
    try:
        user = json.loads(get_jwt_identity())
        product_name = db.session.execute(db.select(products.product_name).where(products.product_id == data["product_id"])).first()
        if not product_name:
            return jsonify({"error": "The product doenst exists."}), 404
        db.session.execute(db.delete(products).where(products.product_id == data["product_id"]))
        log = change_logg(user_id=user["id"], log=f"{user["name"]} deleted a product: {product_name[0]}")
        db.session.add(log)
        db.session.commit()
        return jsonify({"message": "Product deleted!"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500
    
@bp_product.route("/products/<int:ID>", methods=["GET"])
@jwt_required()
def get_product_id(ID):
    """
    Returns the product with the given ID, error message if the product doesnt exists.

    ### Endpoint:
    - Method: GET
    - URL: /products/<id:int>
    - Content-type: JSON

    ### Authorization:
    - This endpoint is protected by JWT validation.

    ### Header example:

        {"Authorization": "Bearer {JWT-HERE}"}

    ### Responses:

    - 200 Ok

        {
            "product_id": 1,
            "product_name": "some name",
            "price" : 1500.0,
            "category" : "some category",
            "description" : "some description",
            "available" : True
        }

    - 404 Not found

        {"error": "Product not found"}

    - 400 Bad request

        {"error" : "ID must be a positive integer"}
    
    - 500 Internal server error

        {"error" : "Internal server error"}
    """
    
    if not isinstance(ID, int) or ID < 0:
        return jsonify({"error" : "ID must be a positive integer"}), 400
    
    try:
        product = db.session.query(products).where(products.product_id == ID).first()
        if product is None:
            return jsonify({"error": "Product not found."}), 404
        else:
            return jsonify(product.toDict()), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error" : "Internal server error"}), 500


@bp_product.route("/products/changelog", methods=["GET"])
@jwt_required()
def get_log():
    """
        Returns a list of changes. This endpoint is protected by JWT validation.

        ### Endpoint
        - Method: GET
        - URL: /products/changelog

        ### Authorization
        - This endpoint is protected by JWT validation

        ### Header example:

            {"Authorization": "Bearer {JWT-HERE}"}


        ### Response:
        Content-type: JSON

        - 200 Ok

            [
                {
                    "log_id": 0, 
                    "user_id": 1, 
                    "log": "someaction", 
                    "date": "2025-01-16T12:00:00Z"
                }
            ]

        - 500 Internal error

            {"error": "Internal server error"}
    """
    try:
        logs = db.session.query(change_logg).order_by(change_logg.id_log.desc()).all()
        log_list = [log.toDict() for log in logs]
        return jsonify(log_list), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    