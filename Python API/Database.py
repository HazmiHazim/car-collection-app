import mysql.connector
import json
import os
from Logger import Logger

class Database:
    
    def __init__(self) -> None:
        # Load credentials from json file
        with open(os.path.join("f:/Others/Car Collection Project/Python Api/", "DBCredentials.json"), "r") as file:
            credentials = json.load(file)
        self.host = credentials["mysql"]["host"]
        self.user = credentials["mysql"]["user"]
        self.password = credentials["mysql"]["password"]
        self.database_name = credentials["mysql"]["database"]
        # Create an instance class of Logger
        self.logger = Logger()
        # Initialize table as dictionary
        self.tables = {}
        
    def db_connection(self):
        try:
            connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database_name
            )
            return connection
                
        except Exception as error:
            self.logger.debug(error)
        
    def create_tables(self):
        try:
            connection = self.db_connection()
            self.tables["users"] = (
                "CREATE TABLE IF NOT EXISTS `users` ("
                "`id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,"
                "`email` varchar(255) NOT NULL,"
                "`password` varchar(255) NOT NULL,"
                "`created_at` timestamp NULL DEFAULT NULL,"
                "`updated_at` timestamp NULL DEFAULT NULL,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
            )
            
            self.tables["cars"] = (
                "CREATE TABLE IF NOT EXISTS `cars` ("
                "`id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,"
                "`name` varchar(255) DEFAULT NULL,"
                "`model` varchar(255) DEFAULT NULL,"
                "`description` text DEFAULT NULL,"
                "`image` varchar(255) DEFAULT NULL,"
                "`brand_id` bigint(20) UNSIGNED DEFAULT NULL,"
                "`category_id` bigint(20) UNSIGNED DEFAULT NULL,"
                "`created_at` timestamp NULL DEFAULT NULL,"
                "`updated_at` timestamp NULL DEFAULT NULL,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
            )
            
            self.tables["brands"] = (
                "CREATE TABLE IF NOT EXISTS `brands` ("
                "`id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,"
                "`name` varchar(255) NOT NULL,"
                "`image` varchar(255) DEFAULT NULL,"
                "`created_at` timestamp NULL DEFAULT NULL,"
                "`updated_at` timestamp NULL DEFAULT NULL,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
            )
            
            self.tables["categories"] = (
                "CREATE TABLE IF NOT EXISTS `categories` ("
                "`id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,"
                "`name` varchar(255) NOT NULL,"
                "`created_at` timestamp NULL DEFAULT NULL,"
                "`updated_at` timestamp NULL DEFAULT NULL,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
            )
            
            self.tables["colours"] = (
                "CREATE TABLE IF NOT EXISTS `colours` ("
                "`id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,"
                "`name` varchar(255) NOT NULL,"
                "`hex` varchar(7) NOT NULL,"
                "`created_at` timestamp NULL DEFAULT NULL,"
                "`updated_at` timestamp NULL DEFAULT NULL,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
            )
            
            self.tables["car_colours"] = (
                "CREATE TABLE IF NOT EXISTS `car_colours` ("
                "car_id bigint(20) UNSIGNED NOT NULL,"
                "colour_id bigint(20) UNSIGNED NOT NULL,"
                "FOREIGN KEY (car_id) REFERENCES cars(id) ON UPDATE CASCADE,"
                "FOREIGN KEY (colour_id) REFERENCES colours(id) ON UPDATE CASCADE,"
                "`created_at` timestamp NULL DEFAULT NULL,"
                "`updated_at` timestamp NULL DEFAULT NULL"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
            )
            
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()
            for table_name in self.tables:
                create_definition = self.tables[table_name]
                cursor.execute(create_definition)
            # Close cursor and connection
            cursor.close()
            connection.close()
            
        except Exception as error:
            self.logger.debug(error)
            
if __name__ == "__main__":
    db_instance = Database()
    db_instance.create_tables()