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
                return 405
            
            car_name = request.args.get("car_name")
            car_model =  request.args.get("car_model")
            car_description = request.args.get("car_description")
            brand_id = 1
            category_id = 1
            created_at = datetime.now()
            updated_at = datetime.now()
            
            if not all([car_name, car_model, car_description, brand_id, category_id]):
                return 400
            
            # Make connection to Database
            connection = self.database.db_connection()
            cursor = connection.cursor()
            query = (
                "INSERT INTO cars "
                "(name, model, description, brand_id, category_id, created_at, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            data = (car_name, car_model, car_description, brand_id, category_id, created_at, updated_at)
            cursor.execute(query, data)
            
            # Make sure data is committed to the database
            connection.commit()
            cursor.close()
            connection.close()
        
        except Exception as error:
            self.logger.debug(error)
            
            
api_instance = Api()
@api_instance.app.route("/api/create_car", methods=["POST"])
def api_create_car():
    return api_instance.create_car()
            
if __name__ == "__main__":
    api_instance.app.run(debug=True)