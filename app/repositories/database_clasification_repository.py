
import json
from fastapi import HTTPException
from mysql.connector import Error
from datetime import datetime
from app.infrastructure.database_dlp_connection import DataBaseDlpConnection
from app.models.database_persistence_entity import DatabasePersistenceEntity
from app.models.information_classification_entity import InformationClassificationEntity
from app.models.historic_scan_entity import HistoricScanEntity
from app.infrastructure.database_persistence_connection import DataBasePersistenceConnection as dbpc

class DataBaseClasificationRepository():
    def __init__(self):
        pass

    def check_database_existence(id_database):
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()

            query = f"""
                SELECT id, host, username, password, port
                FROM database_persistence
                WHERE id = {id_database}
                """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            main_db_connection.close()

            if result:
                return DatabasePersistenceEntity(
                    id = result[0],
                    host = result[1],
                    username = result[2],
                    password = result[3],
                    port = result[4],
                )
            else:
                return None
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e

    def get_database_names(data_connection: DatabasePersistenceEntity):
        try:
            connection_database = dbpc(
                host = data_connection.host, 
                user = data_connection.username, 
                password = data_connection.password, 
                port = data_connection.port
            )
            
            conn = connection_database.connect()

            if connection_database.is_connected():
                cursor = conn.cursor()
                cursor.execute("SHOW DATABASES")

                databases = [db[0] for db in cursor.fetchall()]

                cursor.close()
                connection_database.close()
                return databases
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e
        
    def get_database_excluded():
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()

            query = """
                SELECT id, database_name
                FROM excluded_database
                """
            
            cursor.execute(query)
            excluded_databases = cursor.fetchall()
            excluded_list = [db[1] for db in excluded_databases]
            cursor.close()
            main_db_connection.close()

            return excluded_list
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e

    def get_information_expression():
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()

            query = """
                SELECT id, information_type, information_expression, id_user
                FROM information_classification
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            main_db_connection.close()

            information_classifications = []
            for result in results:
                information_classifications.append(InformationClassificationEntity(
                    id = result[0],
                    information_type = result[1],
                    information_expression = result[2],
                    user_id = result[3],
                ))

            return information_classifications
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e
        
    def get_database_tables(data_connection: DatabasePersistenceEntity, database):
        try:
            connection_database = dbpc(
                host = data_connection.host, 
                user = data_connection.username, 
                password = data_connection.password, 
                port = data_connection.port
            )
            
            conn = connection_database.connect()
            
            if connection_database.is_connected():
                cursor = conn.cursor()
            
                cursor.execute(f"USE {database}")
            
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall() 
                cursor.close()
                connection_database.close()

                return [table[0] for table in tables]
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e
        
    def get_fields_table(data_connection: DatabasePersistenceEntity, database, table):
        try:
            connection_database = dbpc(
                host = data_connection.host, 
                user = data_connection.username, 
                password = data_connection.password, 
                port = data_connection.port
            )
            
            conn = connection_database.connect()   

            if connection_database.is_connected():
                cursor = conn.cursor()
                cursor.execute(f"USE {database}")
            
                cursor.execute(f"SHOW COLUMNS FROM {table}")
                fields = cursor.fetchall()

                field_names = [field[0] for field in fields]

                cursor.close()
                connection_database.close()

                return field_names

        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e
        
    def insert_historic_scan(id_database: int, classification: dict, date_scan: str, id_user: int):
        try:
            date_scan_obj = datetime.strptime(date_scan, '%Y-%m-%d %H:%M:%S')
            classification_str = json.dumps(classification)

            historic_scan = HistoricScanEntity(
                date_scan = date_scan_obj,
                classification = classification_str,
                id_database = id_database,
                deleted = 0,
                user_id = id_user
            )

            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()

            insert_query = """
                INSERT INTO historic_scan (date_scan, classification, id_database, deleted, id_user)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (historic_scan.date_scan, historic_scan.classification, historic_scan.id_database, historic_scan.deleted, historic_scan.user_id))
            main_db_connection.commit()
            inserted_id = cursor.lastrowid
            cursor.close()
            main_db_connection.close()

            return inserted_id

        except Error as e:
            raise HTTPException(status_code=500, detail="Error to insert record in table") from e

        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e
        
    def search_historic_scan(id_database: int, deleted: int = None):
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()

            query = """
                SELECT id, date_scan, classification, id_database, deleted, id_user
                FROM historic_scan
                WHERE id_database = %s
            """
            if deleted is not None:
                query += " AND deleted = %s"
                cursor.execute(query, (id_database, deleted))
            else:
                cursor.execute(query, (id_database,))
                
            results = cursor.fetchall()
            cursor.close()
            main_db_connection.close()
            
            historic_scan_list = []
            
            for result in results:
                historic_scan_list.append(HistoricScanEntity(
                    id = result[0],
                    date_scan = result[1],
                    classification = result[2],
                    id_database = result[3],
                    deleted = result[4],
                    user_id = result[5],
                ))

            return historic_scan_list
        except Error as e:
            raise HTTPException(status_code=500, detail="Error to search record in table") from e
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e
    
    def update_historic_scan(id_database: int):
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()

            query = """
                UPDATE historic_scan hs
                JOIN (
                    SELECT MAX(date_scan) AS max_date_scan
                    FROM historic_scan
                    WHERE id_database = %s
                ) AS subquery
                ON hs.date_scan = subquery.max_date_scan
                SET hs.deleted = 1
                WHERE hs.id_database = %s
            """
            cursor.execute(query, (id_database, id_database))
            main_db_connection.commit()

            cursor.close()
            main_db_connection.close()

            return {"message": "Record updated successfully."}

        except Error as e:
            raise HTTPException(status_code=500, detail=f"{e}") from e

        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e
        
    def insert_information_classification(data_type, expression, user_id):
        try:
            db_connection = DataBaseDlpConnection()
            main_db_connection = db_connection.connect()
            cursor = main_db_connection.cursor()
            
            insert_query = """
                INSERT INTO information_classification (information_type, information_expression, id_user)
                VALUES (%s, %s, %s);
            """
            cursor.execute(insert_query, (data_type, expression, user_id))
            main_db_connection.commit()
            cursor.close()
            main_db_connection.close()
            
            return {"message": "Record insert successfully."}
        except Error as e:
            raise HTTPException(status_code=500, detail=f"{e}") from e

        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") from e    