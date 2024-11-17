from fastapi import HTTPException
from app.dtos.request_data_base import RequestDataBase
from app.infrastructure.database_persistence_connection import DataBasePersistenceConnection as dbpc
from app.infrastructure.database_dlp_connection import DataBaseDlpConnection
from app.models.database_persistence_entity import DatabasePersistenceEntity

class DataBasePersistenceRepository:
    def __init__(self):
        pass

    def check_database_persistence(data: RequestDataBase):
        connection_database = dbpc(
            host = data.host, 
            user = data.user_name, 
            password = data.password, 
            port = data.port
        )
        return connection_database.check_connection()

    def insert_data_persistence(data: DatabasePersistenceEntity):
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()

            insert_query = """
                INSERT INTO database_persistence (host, username, password, port) 
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(insert_query, (data.host, data.username, data.password, data.port))
            main_db_connection.commit()

            inserted_id = cursor.lastrowid

            cursor.close()
            main_db_connection.close()
        
            return inserted_id
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e