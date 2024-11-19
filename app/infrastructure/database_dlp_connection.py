import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class DataBaseDlpConnection:
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST')
        self.user = os.getenv('MYSQL_USER')
        self.port = os.getenv('MYSQL_PORT')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.database = os.getenv('MYSQL_DATABASE')
        self.connection = None

    def connect(self):
        if not self.connection:
            try:
                self.connection = mysql.connector.connect(
                    host = self.host,
                    user = self.user,
                    port = self.port,
                    password = self.password,
                    database = self.database
                )
            except mysql.connector.Error as err:
                raise

        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()