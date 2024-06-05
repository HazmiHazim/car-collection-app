import re
from flask import Flask
from flask import request
from Database import Database
from Logger import Logger
from datetime import datetime

class Api:
    
    def __init__(self) -> None:
        self.app = Flask(__name__)
        # Create an instance class of DBConnection
        self.database = Database()
        # Create an instance class of Logger
        self.logger = Logger()
        
    def create_car(self):
        connection = None
        cursor = None
        try:
            if request.method != "POST":
                return "Method Not Allowed", 405
            
            car_name = request.args.get("car_name")
            car_model =  request.args.get("car_model")
            car_description = request.args.get("car_description")
            car_image = request.args.get("car_image")
            brand_id = request.args.get("brand_id")
            category_id = request.args.get("category_id")
            created_at = datetime.now()
            updated_at = datetime.now()
            
            if not all([car_name, car_model, car_description, car_image, brand_id, category_id]):
                return "Bad Request - Missing Parameters", 400
            
            # Make connection to Database
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = (
                "INSERT INTO cars "
                "(name, model, description, image, brand_id, category_id, created_at, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            data = (car_name, car_model, car_description, car_image, brand_id, category_id, created_at, updated_at)
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
            
    def retrieve_all_cars(self):
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
            
            return cars, 200
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
            
    def retrieve_specific_car(self, id):
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
                return car, 200
            else:
                return f"Car for id = {id} not found", 404
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
            
    def update_specific_car(self, id):
        connection = None
        cursor = None
        try:
            if request.method not in ["POST", "PUT"]:
                return "Method Not Allowed", 405
            
            car_name = request.args.get("car_name")
            car_model =  request.args.get("car_model")
            car_description = request.args.get("car_description")
            car_image = request.args.get("car_image")
            brand_id = request.args.get("brand_id")
            category_id = request.args.get("category_id")
            
            # Create a dictionary for dynamic update query
            update_fields = {}
            if car_name:
                update_fields["name"] = car_name
            
            if car_model:
                update_fields["model"] = car_model
                
            if car_description:
                update_fields["description"] = car_description
                
            if car_image:
                update_fields["image"] = car_image
                
            if brand_id:
                update_fields["brand_id"] = brand_id
                
            if category_id:
                update_fields["category_id"] = category_id
                
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
            
    def delete_specific_car(self, id):
        connection = None
        cursor = None
        try:
            if request.method != "DELETE":
                return "Method Not Allowed", 405
            
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = "DELETE FROM cars WHERE id = %s"
            cursor.execute(query, (id,))
            
            if cursor.rowcount > 0:
                connection.commit()
                return "Deleted successfully.", 200
            else:
                return f"Delete failed. Car for id = {id} not found", 404
            
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
            
    def create_brand(self):
        connection = None
        cursor = None
        try:
            if request.method != "POST":
                return "Method Not Allowed", 405
            
            brand_name = request.args.get("brand_name")
            brand_image = request.args.get("brand_image")
            created_at = datetime.now()
            updated_at = datetime.now()
            
            if not all([brand_name, brand_image]):
                return "Bad Request - Missing Parameters", 400
            
            # Make connection to Database
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = (
                "INSERT INTO brands "
                "(name, image, created_at, updated_at)"
                "VALUES (%s, %s, %s, %s)"
            )
            data = (brand_name, brand_image, created_at, updated_at)
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
            
    def retrieve_all_brands(self):
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
            
            return brands, 200
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
            
    def retrieve_specific_brand(self, id):
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
                return brand, 200
            else:
                return f"Brand for id = {id} not found", 404
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
            
    def update_specific_brand(self, id):
        connection = None
        cursor = None
        try:
            if request.method not in ["POST", "PUT"]:
                return "Method Not Allowed", 405
            
            brand_name = request.args.get("brand_name")
            brand_image =  request.args.get("brand_image")
            
            # Create a dictionary for dynamic update query
            update_fields = {}
            if brand_name:
                update_fields["name"] = brand_name
            
            if brand_image:
                update_fields["image"] = brand_image
                
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
                
    def delete_specific_brand(self, id):
        connection = None
        cursor = None
        try:
            if request.method != "DELETE":
                return "Method Not Allowed", 405
            
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = "DELETE FROM brands WHERE id = %s"
            cursor.execute(query, (id,))
            
            if cursor.rowcount > 0:
                connection.commit()
                return "Deleted successfully.", 200
            else:
                return f"Delete failed. Brand for id = {id} not found", 404
            
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                
    def create_category(self):
        connection = None
        cursor = None
        try:
            if request.method != "POST":
                return "Method Not Allowed", 405
            
            category_name = request.args.get("category_name")
            created_at = datetime.now()
            updated_at = datetime.now()
            
            if not category_name:
                return "Bad Request - Missing Parameters", 400
            
            # Make connection to Database
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = (
                "INSERT INTO categories "
                "(name, created_at, updated_at)"
                "VALUES (%s, %s, %s)"
            )
            data = (category_name, created_at, updated_at)
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
                
    def retrieve_all_categories(self):
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
            
            return categories, 200
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                
    def retrieve_specific_category(self, id):
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
                return category, 200
            else:
                return f"Category for id = {id} not found", 404
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                
    def update_specific_category(self, id):
        connection = None
        cursor = None
        try:
            if request.method not in ["POST", "PUT"]:
                return "Method Not Allowed", 405
            
            category_name = request.args.get("category_name")
            
            # Create a dictionary for dynamic update query
            update_fields = {}
            if category_name:
                update_fields["name"] = category_name
                
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
                
    def delete_specific_category(self, id):
        connection = None
        cursor = None
        try:
            if request.method != "DELETE":
                return "Method Not Allowed", 405
            
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = "DELETE FROM categories WHERE id = %s"
            cursor.execute(query, (id,))
            
            if cursor.rowcount > 0:
                connection.commit()
                return "Deleted successfully.", 200
            else:
                return f"Delete failed. Category for id = {id} not found", 404
            
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                
    def create_colour(self):
        connection = None
        cursor = None
        try:
            if request.method != "POST":
                return "Method Not Allowed", 405
            
            colour_name = request.args.get("colour_name")
            hex_code = request.args.get("hex_code")
            created_at = datetime.now()
            updated_at = datetime.now()
            
            if not all([colour_name, hex_code]):
                return "Bad Request - Missing Parameters", 400
            
            # Regular expression to match hex colour code entered by user
            hex_pattern = re.compile(r"^#?([a-f0-9]{6}|[a-f0-9]{3})$")
            
            # Check if the hex code entered by user is valid format
            if not hex_pattern.match(hex_code):
                return "Invalid hex code", 400
            
            # Make connection to Database
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = (
                "INSERT INTO colours "
                "(name, hex, created_at, updated_at)"
                "VALUES (%s, %s, %s, %s)"
            )
            data = (colour_name, hex_code, created_at, updated_at)
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
                
    def retrieve_all_colours(self):
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
            
            return colours, 200
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                
    def retrieve_specific_colour(self, id):
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
                return colour, 200
            else:
                return f"Colour for id = {id} not found", 404
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                
    def update_specific_colour(self, id):
        connection = None
        cursor = None
        try:
            if request.method not in ["POST", "PUT"]:
                return "Method Not Allowed", 405
            
            colour_name = request.args.get("colour_name")
            hex_code =  request.args.get("hex_code")
            
            # Create a dictionary for dynamic update query
            update_fields = {}
            if colour_name:
                update_fields["name"] = colour_name
            
            # Regular expression to match hex colour code entered by user
            hex_pattern = re.compile(r"^#?([a-f0-9]{6}|[a-f0-9]{3})$")
            
            # Check if the hex code entered by user is valid format
            if hex_code:
                if not hex_pattern.match(hex_code):
                    return "Invalid hex code", 400
                update_fields["hex"] = hex_code
                
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
            
api_instance = Api()
@api_instance.app.route("/api/create_car", methods=["POST"])
def api_create_car():
    return api_instance.create_car()

@api_instance.app.route("/api/all_cars", methods=["GET"])
def api_retrieve_all_cars():
    return api_instance.retrieve_all_cars()

@api_instance.app.route("/api/car/<id>", methods=["GET"])
def api_retrieve_specific_car(id):
    return api_instance.retrieve_specific_car(id)

@api_instance.app.route("/api/update_car/<id>", methods=["PUT", "POST"])
def api_update_specific_car(id):
    return api_instance.update_specific_car(id)

@api_instance.app.route("/api/delete_car/<id>", methods=["DELETE"])
def api_delete_specific_car(id):
    return api_instance.delete_specific_car(id)

@api_instance.app.route("/api/create_brand", methods=["POST"])
def api_create_brand():
    return api_instance.create_brand()

@api_instance.app.route("/api/all_brands", methods=["GET"])
def api_retrieve_all_brands():
    return api_instance.retrieve_all_brands()

@api_instance.app.route("/api/brand/<id>", methods=["GET"])
def api_retrieve_specific_brand(id):
    return api_instance.retrieve_specific_brand(id)

@api_instance.app.route("/api/update_brand/<id>", methods=["PUT", "POST"])
def api_update_specific_brand(id):
    return api_instance.update_specific_brand(id)

@api_instance.app.route("/api/delete_brand/<id>", methods=["DELETE"])
def api_delete_specific_brand(id):
    return api_instance.delete_specific_brand(id)

@api_instance.app.route("/api/create_category", methods=["POST"])
def api_create_category():
    return api_instance.create_category()

@api_instance.app.route("/api/all_categories", methods=["GET"])
def api_retrieve_all_categories():
    return api_instance.retrieve_all_categories()

@api_instance.app.route("/api/category/<id>", methods=["GET"])
def api_retrieve_specific_category(id):
    return api_instance.retrieve_specific_category(id)

@api_instance.app.route("/api/update_category/<id>", methods=["PUT", "POST"])
def api_update_specific_category(id):
    return api_instance.update_specific_category(id)

@api_instance.app.route("/api/delete_category/<id>", methods=["DELETE"])
def api_delete_specific_category(id):
    return api_instance.delete_specific_category(id)

@api_instance.app.route("/api/create_colour", methods=["POST"])
def api_create_colour():
    return api_instance.create_colour()

@api_instance.app.route("/api/all_colours", methods=["GET"])
def api_retrieve_all_colours():
    return api_instance.retrieve_all_colours()

@api_instance.app.route("/api/colour/<id>", methods=["GET"])
def api_retrieve_specific_coloury(id):
    return api_instance.retrieve_specific_colour(id)

@api_instance.app.route("/api/update_colour/<id>", methods=["PUT", "POST"])
def api_update_specific_colour(id):
    return api_instance.update_specific_colour(id)
            
if __name__ == "__main__":
    api_instance.app.run(host="0.0.0.0", port=5000, debug=True)