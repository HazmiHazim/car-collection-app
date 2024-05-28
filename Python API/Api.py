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
        try:
            if request.method != "POST":
                return "Method Not Allowed", 405
            
            car_name = request.args.get("car_name")
            car_model =  request.args.get("car_model")
            car_description = request.args.get("car_description")
            car_image = request.args.get("car_image")
            brand_id = 1
            category_id = 1
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
            cursor.close()
            connection.close()
            
    def retrieve_all_cars(self):
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
            cursor.close()
            connection.close()
            
    def retrieve_specific_car(self, id):
        try:
            if request.method != "GET":
                return "Method Not Allowed", 405
            
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = ("SELECT * FROM cars WHERE id = %s")
            cursor.execute(query, (id,))
            car_data = cursor.fetchone()
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
        
        except Exception as error:
            self.logger.debug(error)
            
        finally:
            cursor.close()
            connection.close()
            
api_instance = Api()
@api_instance.app.route("/api/create_car", methods=["POST"])
def api_create_car():
    return api_instance.create_car()

@api_instance.app.route("/api/all_cars", methods=["GET"])
def api_retrieve_all_cars():
    return api_instance.retrieve_all_cars()

@api_instance.app.route("/api/cars/<id>", methods=["GET"])
def api_retrieve_specific_car(id):
    return api_instance.retrieve_specific_car(id)
            
if __name__ == "__main__":
    api_instance.app.run(host="0.0.0.0", port=5000, debug=True)