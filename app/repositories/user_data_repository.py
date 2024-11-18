from fastapi import HTTPException
from mysql.connector import Error
from app.infrastructure.database_dlp_connection import DataBaseDlpConnection

class UserDataRepository:
    def __init__(self):
        pass
    
    def insert_user(username, password):
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()

            insert_query = """
                INSERT INTO user (username, password)
                VALUES (%s, %s)
            """           
            cursor.execute(insert_query, (username, password,))
            main_db_connection.commit()
            inserted_id = cursor.lastrowid
            cursor.close()
            main_db_connection.close()

            return {"user has been saved with id": f"{inserted_id}"}
        except Error as e:
            raise HTTPException(status_code=500, detail="Error to insert record in table") from e

        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e