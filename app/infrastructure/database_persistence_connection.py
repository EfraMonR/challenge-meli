import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException

class DataBasePersistenceConnection:
    def __init__(self, host: str, user: str, password: str, port: int):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def check_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                port = self.port
            )

            if self.connection.is_connected():
                return True
            
        except Error as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e
        
        finally:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                
    def connect(self):
        if not self.connection:
            try:
                self.connection = mysql.connector.connect(
                    host = self.host,
                    user = self.user,
                    port = self.port,
                    password = self.password
                )
            except mysql.connector.Error as err:
                raise

        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()
            
    def is_connected(self):
        return self.connection and self.connection.is_connected()