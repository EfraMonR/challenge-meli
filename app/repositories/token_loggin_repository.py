from fastapi import HTTPException
from app.infrastructure.database_dlp_connection import DataBaseDlpConnection
from app.models.user_data_entity import UserDataEntity

class TokenLoginRepository:
    def __init__(self):
        pass
    
    def search_data_user(user):
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()
            
            query = """
                SELECT id, username, password
                FROM user
                WHERE username = %s
            """
            cursor.execute(query, (user,))
            result = cursor.fetchone()
            cursor.close()
            main_db_connection.close()
            
            if result:
                return UserDataEntity(
                    id = result[0],
                    username = result[1],
                    password = result[2]
                )
            else:
                return None
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e