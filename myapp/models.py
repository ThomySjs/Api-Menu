from .extensions import db
from sqlalchemy import func, ForeignKey, String, Integer, Boolean, Numeric, CheckConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import bcrypt

class users(db.Model):
    __tablename__ = "users"
    """
        Manages the user`s data.

        ### Keys:
        - `user_id (Integer)` Primary key
        - `user_name (String)`
        - `email (String)` Unique
        - `password (String)`
        - `verified (Boolean)`

        ### Methods:
        - toDict() 
        - hash_password()
        - check_password()
    """
    user_id : Mapped[int] = mapped_column(primary_key=True)
    user_name : Mapped[str] = mapped_column(String(50), nullable=False)
    email : Mapped[str] =  mapped_column(String(150), nullable=False, unique=True)
    password : Mapped[str] = mapped_column(String(150), nullable=False)
    verified : Mapped[bool] = mapped_column(Boolean, default=False)
    __table_args__ = {'extend_existing': True} 

    def toDict(self):
        """
            Returns a dictionary containing the users data.

            Example: 
                print(user.toDict()) 

                {
                    "user_id" : 0,
                    "user_name" : somename,
                    "email" : someemai,
                    "password" : supersecretpassword,
                    "verified" : True
                }
        """
        return {
            "user_id" : self.user_id,
            "user_name" : self.user_name,
            "email" : self.email,
            "password" : self.password,
            "verified" : self.verified
        }

    def hash_password(password: str) -> str:
        """
            Hashes and encodes the given password using bcrypt.

            Parameters:
                `password`(str): Plain text password

            Returns:
                Hashed password as a string.

            Example: 
                mypassword = hash_password("supersecretpassword")
                print(mypassword) # hashed
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')
    
    def check_password(password: str, hashed_password: str):
        """
            Compares the plain-text password against the hashed password stored in the database.

            Parameters:
                `password`(str): contains the plain text password.
                `hashed_password`(str): contains the hashed password

            Returns:
                Bool: True if the password matches, False if the password is incorrect.

            Example: 
                is_valid = check_password(`password`, `hashed_password`)

                print(is_valid) # True or False
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def __repr__(self):
        return f"Name: {self.user_name}, Email: {self.email}"

class products(db.Model):
    __tablename__ = "products"
    """
        Manages the product data.

        ### Keys:
        - `product_id (Integer)` Primary key
        - `product_name (String)`
        - `price (Float/Numeric)` Constraint price > 0
        - `description (String)`
        - `category (String)`
        - `available (Boolean)`

        ### Methods:
        - toDict() 
    """
    product_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(150), nullable=False)
    price : Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    description : Mapped[str] = mapped_column(String(250), nullable=False)
    category : Mapped[str] = mapped_column(String(50), nullable=False)
    available : Mapped[bool] = mapped_column(Boolean, default=True)
    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),)

    def toDict(self):
        """
            Returns a dictionary containing the product data.

            Example: 
                print(product.toDict()) 

                {
                    "product_id" : 0,
                    "product_name" : somename,
                    "price" : 1500.0,
                    "description": somedescription,
                    "category": somecategory,
                    "available": True
                }
        """
        return {
                "product_id": self.product_id, 
                "product_name": self.product_name, 
                "price": self.price, 
                "description": self.description,
                "category": self.category,
                "available": self.available
            }
    
    def __repr__(self):
        return f"id: {self.product_id}, product_name : {self.product_name}, price: {self.price}, description : {self.description}, category : {self.category}, available : {self.available}"
    
class change_logg(db.Model):
    __tablename__ = "log"
    """
        Manages changes made in the database.

        ### Keys:
        - `id_log (Integer)` Primary key
        - `user_id (Integer)` Foreign key
        - `log (String)` Change (ex: user deleted a product.)
        - `date (Datetime)`

        ### Methods:
        - toDict() 
    """
    id_log : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    log : Mapped[str] = mapped_column(String(250), nullable=False)
    date : Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def toDict(self):
        """
            Returns a dictionary containing change logs.

            Example: 
                print(log.toDict()) 

                {
                    "log_id": 0, 
                    "user_id": 1, 
                    "log": User added a product., 
                    "date": 2024-12-26 16:32:32
                }
        """
        return {
                "log_id": self.id_log, 
                "user_id": self.user_id, 
                "log": self.log, 
                "date": self.date
            }