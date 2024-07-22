import re
import bcrypt
import uuid
import secrets
import jwt
from flask import Flask
from flask import request, jsonify
from Database import Database
from Logger import Logger
from datetime import datetime, timedelta
from flask_cors import CORS

class Api:
    
    def __init__(self) -> None:
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for Flask app
        # Create an instance class of DBConnection
        self.database = Database()
        # Create an instance class of Logger
        self.logger = Logger()
        # Run routes method
        self.routes()
        
    def routes(self):
    
        @self.app.route("/api/create_car", methods=["POST"])
        def create_car():
            connection = None
            cursor = None
            try:
                if request.method != "POST":
                    return "Method Not Allowed", 405
                
                request_data = request.get_json()
                
                required_keys = [
                    "car_name",
                    "car_model",
                    "car_description",
                    "car_image",
                    "brand_id",
                    "category_id",
                ]
                
                if not all(key in request_data for key in required_keys):
                    return "Bad Request - Missing Parameters", 400
                
                created_at = datetime.now()
                updated_at = datetime.now()
                
                # Make connection to Database
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = (
                    "INSERT INTO cars "
                    "(name, model, description, image, brand_id, category_id, created_at, updated_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                )
                data = (
                    request_data["car_name"],
                    request_data["car_model"],
                    request_data["car_description"],
                    request_data["car_image"],
                    request_data["brand_id"],
                    request_data["category_id"],
                    created_at,
                    updated_at
                )
                cursor.execute(query, data)
                # Make sure data is committed to the database
                connection.commit()
                
                return "Car created successfully.", 200
            
            except Exception as error:
                self.logger.debug(error)
            
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/all_cars", methods=["GET"])
        def retrieve_all_cars():
            connection = None
            cursor = None
            try:
                if request.method != "GET":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = ("SELECT * FROM cars")
                cursor.execute(query)
                car_list_data = cursor.fetchall()
                # Initialize empty list to store dictionaries representing cars
                cars = []
                for car_data in car_list_data:
                    car = {
                        "id": car_data[0],
                        "name": car_data[1],
                        "model": car_data[2],
                        "description": car_data[3],
                        "image": car_data[4],
                        "brand_id": car_data[5],
                        "category_id": car_data[6],
                        "created_at": car_data[7],
                        "updated_at": car_data[8]
                    }
                    cars.append(car)
                
                return jsonify(cars), 200
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
            
        @self.app.route("/api/car/<id>", methods=["GET"])
        def retrieve_specific_car(id):
            connection = None
            cursor = None
            try:
                if request.method != "GET":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = ("SELECT * FROM cars WHERE id = %s")
                cursor.execute(query, (id,))
                car_data = cursor.fetchone()
                # Initialize empty dictionaries
                if car_data:
                    car = {
                        "id": car_data[0],
                        "name": car_data[1],
                        "model": car_data[2],
                        "description": car_data[3],
                        "image": car_data[4],
                        "brand_id": car_data[5],
                        "category_id": car_data[6],
                        "created_at": car_data[7],
                        "updated_at": car_data[8]
                    }
                    return jsonify(car), 200
                else:
                    return f"Car for id = {id} not found", 404
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/update_car/<id>", methods=["PUT", "POST"])        
        def update_specific_car(id):
            connection = None
            cursor = None
            try:
                if request.method not in ["POST", "PUT"]:
                    return "Method Not Allowed", 405
                
                request_data = request.get_json()
                
                # Create a dictionary for dynamic update query
                update_fields = {}
                if "car_name" in request_data:
                    update_fields["name"] = request_data["car_name"]
                
                if "car_model" in request_data:
                    update_fields["model"] = request_data["car_model"]
                    
                if "car_description" in request_data:
                    update_fields["description"] = request_data["car_description"]
                    
                if "car_image" in request_data:
                    update_fields["image"] = request_data["car_image"]
                    
                if "brand_id" in request_data:
                    update_fields["brand_id"] = request_data["brand_id"]
                    
                if "category_id" in request_data:
                    update_fields["category_id"] = request_data["category_id"]
                    
                if not update_fields:
                    return "Please enter at least one field to update.", 400
                
                update_fields["updated_at"] = datetime.now()
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                
                # Return error message if id does not exists
                cursor.execute("SELECT id FROM cars WHERE id = %s", (id,))
                if not cursor.fetchone():
                    return f"Update failed. Car for id = {id} not found.", 404
                
                # Build the SET clause dynamically
                set_clause = ", ".join(f"{key} = %s" for key in update_fields.keys())
                values = list(update_fields.values())
                # Append the id at the end for the WHERE clause
                values.append(id)
                query = f"UPDATE cars SET {set_clause} WHERE id = %s"
                cursor.execute(query, values)
                # Make sure data is committed to the database
                connection.commit()
                return "Updated successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/delete_car/<id>", methods=["DELETE"])        
        def delete_specific_car(id):
            connection = None
            cursor = None
            try:
                if request.method != "DELETE":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = "DELETE FROM cars WHERE id = %s"
                cursor.execute(query, (id,))
                
                if cursor.rowcount == 0:
                    return f"Delete failed. Car for id = {id} not found", 404
                
                connection.commit()
                return "Deleted successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/create_brand", methods=["POST"])   
        def create_brand():
            connection = None
            cursor = None
            try:
                if request.method != "POST":
                    return "Method Not Allowed", 405
                
                request_data = request.get_json()
                
                required_keys = [
                    "brand_name",
                    "brand_image",
                ]
                
                if not all(key in request_data for key in required_keys):
                    return "Bad Request - Missing Parameters", 400
                
                created_at = datetime.now()
                updated_at = datetime.now()
                
                # Make connection to Database
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = (
                    "INSERT INTO brands "
                    "(name, image, created_at, updated_at)"
                    "VALUES (%s, %s, %s, %s)"
                )
                data = (
                    request_data["brand_name"],
                    request_data["brand_image"],
                    created_at,
                    updated_at
                )
                cursor.execute(query, data)
                # Make sure data is committed to the database
                connection.commit()
                
                return "Brand created successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/all_brands", methods=["GET"])   
        def retrieve_all_brands():
            connection = None
            cursor = None
            try:
                if request.method != "GET":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = ("SELECT * FROM brands")
                cursor.execute(query)
                brand_list_data = cursor.fetchall()
                # Initialize empty list to store dictionaries representing cars
                brands = []
                for brand_data in brand_list_data:
                    brand = {
                        "id": brand_data[0],
                        "name": brand_data[1],
                        "image": brand_data[2],
                        "created_at": brand_data[3],
                        "updated_at": brand_data[4]
                    }
                    brands.append(brand)
                
                return jsonify(brands), 200
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/brand/<id>", methods=["GET"])   
        def retrieve_specific_brand(id):
            connection = None
            cursor = None
            try:
                if request.method != "GET":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = ("SELECT * FROM brands WHERE id = %s")
                cursor.execute(query, (id,))
                brand_data = cursor.fetchone()
                # Initialize empty dictionaries
                if brand_data:
                    brand = {
                        "id": brand_data[0],
                        "name": brand_data[1],
                        "image": brand_data[2],
                        "created_at": brand_data[3],
                        "updated_at": brand_data[4]
                    }
                    return jsonify(brand), 200
                else:
                    return f"Brand for id = {id} not found", 404
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/update_brand/<id>", methods=["PUT", "POST"])  
        def update_specific_brand(id):
            connection = None
            cursor = None
            try:
                if request.method not in ["POST", "PUT"]:
                    return "Method Not Allowed", 405
                
                request_data = request.get_json()
                
                # Create a dictionary for dynamic update query
                update_fields = {}
                if "brand_name" in request_data:
                    update_fields["name"] = request_data["brand_name"]
                
                if "brand_image" in request_data:
                    update_fields["image"] = request_data["brand_image"]
                    
                if not update_fields:
                    return "Please enter at least one field to update.", 400
                
                update_fields["updated_at"] = datetime.now()
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                
                # Return error message if id does not exists
                cursor.execute("SELECT id FROM brands WHERE id = %s", (id,))
                if not cursor.fetchone():
                    return f"Update failed. Brand for id = {id} not found.", 404
                
                # Build the SET clause dynamically
                set_clause = ", ".join(f"{key} = %s" for key in update_fields.keys())
                values = list(update_fields.values())
                # Append the id at the end for the WHERE clause
                values.append(id)
                query = f"UPDATE brands SET {set_clause} WHERE id = %s"
                cursor.execute(query, values)
                # Make sure data is committed to the database
                connection.commit()
                return "Updated successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/delete_brand/<id>", methods=["DELETE"])           
        def delete_specific_brand(id):
            connection = None
            cursor = None
            try:
                if request.method != "DELETE":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = "DELETE FROM brands WHERE id = %s"
                cursor.execute(query, (id,))
                
                if cursor.rowcount == 0:
                    return f"Delete failed. Brand for id = {id} not found", 404
                
                connection.commit()
                return "Deleted successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/create_category", methods=["POST"])           
        def create_category():
            connection = None
            cursor = None
            try:
                if request.method != "POST":
                    return "Method Not Allowed", 405
                
                request_data = request.get_json()
                
                created_at = datetime.now()
                updated_at = datetime.now()
                
                if not "category_name" in request_data:
                    return "Bad Request - Missing Parameters", 400
                
                # Make connection to Database
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = (
                    "INSERT INTO categories "
                    "(name, created_at, updated_at)"
                    "VALUES (%s, %s, %s)"
                )
                data = (
                    request_data["category_name"],
                    created_at,
                    updated_at
                )
                cursor.execute(query, data)
                # Make sure data is committed to the database
                connection.commit()
                
                return "Category created successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
       
        @self.app.route("/api/all_categories", methods=["GET"])         
        def retrieve_all_categories():
            connection = None
            cursor = None
            try:
                if request.method != "GET":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = ("SELECT * FROM categories")
                cursor.execute(query)
                category_list_data = cursor.fetchall()
                # Initialize empty list to store dictionaries representing cars
                categories = []
                for category_data in category_list_data:
                    category = {
                        "id": category_data[0],
                        "name": category_data[1],
                        "created_at": category_data[2],
                        "updated_at": category_data[3]
                    }
                    categories.append(category)
                
                return jsonify(categories), 200
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/category/<id>", methods=["GET"])            
        def retrieve_specific_category(id):
            connection = None
            cursor = None
            try:
                if request.method != "GET":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = ("SELECT * FROM categories WHERE id = %s")
                cursor.execute(query, (id,))
                category_data = cursor.fetchone()
                # Initialize empty dictionaries
                if category_data:
                    category = {
                        "id": category_data[0],
                        "name": category_data[1],
                        "created_at": category_data[2],
                        "updated_at": category_data[3]
                    }
                    return jsonify(category), 200
                else:
                    return f"Category for id = {id} not found", 404
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
     
        @self.app.route("/api/update_category/<id>", methods=["PUT", "POST"])           
        def update_specific_category(id):
            connection = None
            cursor = None
            try:
                if request.method not in ["POST", "PUT"]:
                    return "Method Not Allowed", 405
                
                request_data = request.get_json()
                
                # Create a dictionary for dynamic update query
                update_fields = {}
                if "category_name" in request_data:
                    update_fields["name"] = request_data["category_name"]
                    
                if not update_fields:
                    return "Please enter at least one field to update.", 400
                
                update_fields["updated_at"] = datetime.now()
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                
                # Return error message if id does not exists
                cursor.execute("SELECT id FROM categories WHERE id = %s", (id,))
                if not cursor.fetchone():
                    return f"Update failed. Category for id = {id} not found.", 404
                
                # Build the SET clause dynamically
                set_clause = ", ".join(f"{key} = %s" for key in update_fields.keys())
                values = list(update_fields.values())
                # Append the id at the end for the WHERE clause
                values.append(id)
                query = f"UPDATE categories SET {set_clause} WHERE id = %s"
                cursor.execute(query, values)
                # Make sure data is committed to the database
                connection.commit()
                return "Updated successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/delete_category/<id>", methods=["DELETE"])         
        def delete_specific_category(id):
            connection = None
            cursor = None
            try:
                if request.method != "DELETE":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = "DELETE FROM categories WHERE id = %s"
                cursor.execute(query, (id,))
                
                if cursor.rowcount == 0:
                    return f"Delete failed. Category for id = {id} not found", 404
                
                connection.commit()
                return "Deleted successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
     
        @self.app.route("/api/create_colour", methods=["POST"])           
        def create_colour():
            connection = None
            cursor = None
            try:
                if request.method != "POST":
                    return "Method Not Allowed", 405
                
                request_data = request.get_json()
                
                required_keys = [
                    "colour_name",
                    "hex_code",
                ]
                
                if not all(key in request_data for key in required_keys):
                    return "Bad Request - Missing Parameters", 400
                
                created_at = datetime.now()
                updated_at = datetime.now()
                
                # Regular expression to match hex colour code entered by user
                hex_pattern = re.compile(r"^#([a-f0-9]{6}|[a-f0-9]{3})$", re.IGNORECASE)
                
                # Check if the hex code entered by user is valid format
                if not hex_pattern.match(request_data["hex_code"]):
                    return "Invalid hex code", 400
                
                # Make connection to Database
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = (
                    "INSERT INTO colours "
                    "(name, hex, created_at, updated_at)"
                    "VALUES (%s, %s, %s, %s)"
                )
                data = (
                    request_data["colour_name"],
                    request_data["hex_code"],
                    created_at,
                    updated_at
                )
                cursor.execute(query, data)
                # Make sure data is committed to the database
                connection.commit()
                
                return "Colour created successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
     
        @self.app.route("/api/all_colours", methods=["GET"])           
        def retrieve_all_colours():
            connection = None
            cursor = None
            try:
                if request.method != "GET":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = ("SELECT * FROM colours")
                cursor.execute(query)
                colour_list_data = cursor.fetchall()
                # Initialize empty list to store dictionaries representing cars
                colours = []
                for colours_data in colour_list_data:
                    colour = {
                        "id": colours_data[0],
                        "name": colours_data[1],
                        "hex": colours_data[2],
                        "created_at": colours_data[3],
                        "updated_at": colours_data[4]
                    }
                    colours.append(colour)
                
                return jsonify(colours), 200
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
         
        @self.app.route("/api/colour/<id>", methods=["GET"])       
        def retrieve_specific_colour(id):
            connection = None
            cursor = None
            try:
                if request.method != "GET":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = ("SELECT * FROM colours WHERE id = %s")
                cursor.execute(query, (id,))
                colour_data = cursor.fetchone()
                # Initialize empty dictionaries
                if colour_data:
                    colour = {
                        "id": colour_data[0],
                        "name": colour_data[1],
                        "hex": colour_data[2],
                        "created_at": colour_data[3],
                        "updated_at": colour_data[4]
                    }
                    return jsonify(colour), 200
                else:
                    return f"Colour for id = {id} not found", 404
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
    
        @self.app.route("/api/update_colour/<id>", methods=["PUT", "POST"])        
        def update_specific_colour(id):
            connection = None
            cursor = None
            try:
                if request.method not in ["POST", "PUT"]:
                    return "Method Not Allowed", 405
                
                request_data = request.get_json()
                
                # Create a dictionary for dynamic update query
                update_fields = {}
                if "colour_name" in request_data:
                    update_fields["name"] = request_data["colour_name"]
                
                # Regular expression to match hex colour code entered by user
                hex_pattern = re.compile(r"^#([a-f0-9]{6}|[a-f0-9]{3})$", re.IGNORECASE)
                
                # Check if the hex code entered by user is valid format
                if "hex_code" in request_data:
                    if not hex_pattern.match(request_data["hex_code"]):
                        return "Invalid hex code", 400
                    update_fields["hex"] = request_data["hex_code"]
                    
                if not update_fields:
                    return "Please enter at least one field to update.", 400
                
                update_fields["updated_at"] = datetime.now()
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                
                # Return error message if id does not exists
                cursor.execute("SELECT id FROM colours WHERE id = %s", (id,))
                if not cursor.fetchone():
                    return f"Update failed. Colour for id = {id} not found.", 404
                
                # Build the SET clause dynamically
                set_clause = ", ".join(f"{key} = %s" for key in update_fields.keys())
                values = list(update_fields.values())
                # Append the id at the end for the WHERE clause
                values.append(id)
                query = f"UPDATE colours SET {set_clause} WHERE id = %s"
                cursor.execute(query, values)
                # Make sure data is committed to the database
                connection.commit()
                return "Updated successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
         
        @self.app.route("/api/delete_colour/<id>", methods=["DELETE"])       
        def delete_specific_colour(id):
            connection = None
            cursor = None
            try:
                if request.method != "DELETE":
                    return "Method Not Allowed", 405
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = "DELETE FROM colours WHERE id = %s"
                cursor.execute(query, (id,))
                
                if cursor.rowcount == 0:
                    return f"Delete failed. Colour for id = {id} not found", 404
                
                connection.commit()
                return "Deleted successfully.", 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
       
        @self.app.route("/api/auth", methods=["POST"])         
        def authenticate_user():
            connection = None
            cursor = None
            try:
                if request.method != "POST":
                    return "Method Not Allowed", 405
                
                auth_data = request.get_json()
                
                required_keys = [
                    "email",
                    "password",
                ]
                
                if not all(key in auth_data for key in required_keys):
                    return "Bad Request - Missing Parameters", 400
                
                email = auth_data["email"]
                password = auth_data["password"]
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                query = "SELECT * FROM users where email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                
                if not user:
                    return "Email does not exists in the record.", 401
                
                email = user[1]
                password_db = user[2]
                
                # Converting entered password to bytes 
                encoded_password = password.encode("utf-8")
                # Convert password in db to bytes
                
                encoded_password_db = password_db.encode("utf-8")
                # Checking password entered with the password in db
                correct_password = bcrypt.checkpw(encoded_password, encoded_password_db)
                
                if not correct_password:
                    return "Password is not matching with our record.", 401
                
                # Get current time
                current_time = datetime.now()
                
                # Invalidate old tokens
                token_query = "SELECT * FROM access_tokens where email = %s"
                cursor.execute(token_query, (email,))
                old_token = cursor.fetchone()
                if old_token:
                    # Make old_token mutable
                    mutable_old_token = list(old_token)
                    mutable_old_token[5] = current_time
                    mutable_old_token[6] = current_time
                    # Add expired token to expired token table
                    query = (
                        "INSERT INTO expired_access_tokens "
                        "(jti, token, email, created_at, updated_at, expired_at) "
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                    )
                    
                    data = (
                        old_token[1],
                        old_token[2],
                        old_token[3],
                        old_token[4],
                        mutable_old_token[5],
                        mutable_old_token[6]
                    )
                    
                    cursor.execute(query, data)
                    # Make sure data is committed to the database
                    connection.commit()
                    # Delete old token in access token table
                    cursor.execute("DELETE FROM access_tokens WHERE email = %s", (email,))
                    connection.commit()
                    
                # Create new token
                secret_key = secrets.token_hex(32)
                jti = uuid.uuid4().hex
                created_at = current_time
                updated_at = current_time
                expired_at = current_time + timedelta(days=1)
                
                jwt_payload = {
                    "jti": jti,
                    "exp": expired_at,
                    "email": email,
                }
                
                token = jwt.encode(jwt_payload, secret_key, algorithm="HS256")
                # Save token in access token table
                query = (
                    "INSERT INTO access_tokens "
                    "(jti, token, email, created_at, updated_at, expired_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
                
                new_data = (
                    jti,
                    token,
                    email,
                    created_at,
                    updated_at,
                    expired_at
                )
                
                cursor.execute(query, new_data)
                # Make sure data is committed to the database
                connection.commit()
                
                return jsonify(status="success", token=token), 200
                
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()
                    
        @self.app.route("/api/logout", methods=["POST"])         
        def logout_user():
            connection = None
            cursor = None
            try:
                if request.method != "POST":
                    return "Method Not Allowed", 405
                
                headers = request.headers["Authorization"]
                token = headers.split()[1]
                if not token:
                    return "Logout failed - User Unauthorized.", 401
                
                connection = self.database.db_connection()
                cursor = connection.cursor()
                find_query = "SELECT * FROM access_tokens where token = %s"
                cursor.execute(find_query, (token,))
                token_data = cursor.fetchone()
                if not token_data:
                    return "Forbidden - Token expired or not found.", 403
                
                # Make token mutable
                mutable_token_data = list(token)
                # Get current time to update field updated_at and expired_at
                current_time = datetime.now()
                mutable_token_data[5] = current_time
                mutable_token_data[6] = current_time
                
                # Add expired token to expired token table
                insert_query = (
                    "INSERT INTO expired_access_tokens "
                    "(jti, token, email, created_at, updated_at, expired_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
                
                data = (
                    token_data[1],
                    token_data[2],
                    token_data[3],
                    token_data[4],
                    mutable_token_data[5],
                    mutable_token_data[6]
                )
                
                cursor.execute(insert_query, data)
                # Make sure data is committed to the database
                connection.commit()
                # Delete old token in access token table
                cursor.execute("DELETE FROM access_tokens WHERE token = %s", (token,))
                connection.commit()
                
                return "Logout successful.", 200
                
            
            except Exception as error:
                self.logger.debug(error)
                
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    connection.close()

# Run flask
if __name__ == "__main__":
    api_instance = Api()
    api_instance.app.run(host="0.0.0.0", port=5000, debug=True)