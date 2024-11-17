import re
from datetime import datetime
from fastapi import HTTPException
from app.repositories.database_clasification_repository import DataBaseClasificationRepository as dbcr
from app.models.database_persistence_entity import DatabasePersistenceEntity
from app.dtos.response_get_classification import ResponseGetClassification
from app.utils.encryption import EncryptionUtils

def database_clasification(id_database):
    validation_database = dbcr.check_database_existence(id_database)

    if(validation_database is not None):
        decrypted_host = EncryptionUtils.decrypt(validation_database.host)
        decrypted_username = EncryptionUtils.decrypt(validation_database.username)
        decrypted_password = EncryptionUtils.decrypt(validation_database.password)
        decrypted_port = EncryptionUtils.decrypt(validation_database.port)

        decrypted_data = DatabasePersistenceEntity(
            id = validation_database.id,
            host = decrypted_host,
            username = decrypted_username,
            password = decrypted_password,
            port = decrypted_port
        )

        database_names = database_filtered(decrypted_data)
        classification_keywords = information_expression()
        classification_json = field_database_classification(decrypted_data, database_names, classification_keywords)
        id_saved_scan = save_scan(id_database, classification_json)
        
        return {"the historical classification record has been saved with id": f"{id_saved_scan}"}
    else:
        raise HTTPException(status_code = 400, detail="The identifier is not associated with any existing database")

def database_filtered(decrypted_data):
    database_names = dbcr.get_database_names(decrypted_data)
    database_excluded = dbcr.get_database_excluded()

    if database_excluded is None:
        database_excluded = []

    filtered_database_names = [db for db in database_names if db not in database_excluded]
    return filtered_database_names

def information_expression():
    return dbcr.get_information_expression()

def field_database_classification(decrypted_data, database_names, classification_keywords):
    info_json = []
    for database in database_names:
        tables_name = tables_database(decrypted_data, database)
        field_tables_classification = []
        general_info = {}

        for table in tables_name:
            fields_name = field_tables_database(decrypted_data, database, table)
            classification_field = field_classification(fields_name, classification_keywords)
            field_tables = { "nametable" : f"{table}" }
            field_tables["fields"] = classification_field
            field_tables_classification.append(field_tables)

        general_info["databasename"] = database
        general_info["tables"] = field_tables_classification
        info_json.append(general_info)
    
    return info_json

def tables_database(decrypted_data, database):
    return dbcr.get_database_tables(decrypted_data, database)

def field_tables_database(decrypted_data, database, table):
    return dbcr.get_fields_table(decrypted_data, database, table)

def field_classification(field_tables, classification_keywords):
    classification_list = []
    for field in field_tables:
        value = None

        for key in classification_keywords:
            find_expression = re.search(key.information_type, field)
            if find_expression is not None:
                value = { field : key.information_expression }
                classification_list.append(value)

        if value is None:
            value = { field : "N/A" }
            classification_list.append(value)
    return classification_list

def save_scan(id_database, classification):
    time = datetime.now()
    date = time.strftime("%Y-%m-%d %H:%M:%S")
    
    validate_record = dbcr.search_historic_scan(id_database)
    
    if(len(validate_record) > 0):
        dbcr.update_historic_scan(id_database)
    
    return dbcr.insert_historic_scan(id_database, classification, date)

def get_last_scan(id_database):
    validation_database = dbcr.check_database_existence(id_database)
    if(validation_database is not None):
        last_scan = dbcr.search_historic_scan(id_database, 0)
        response = [
            {
                key: value 
                for key, value in ResponseGetClassification.from_entity(scan).__dict__.items() 
                if key not in ['deleted', 'id']
            }
            for scan in last_scan
        ]
        return response
    else:
        raise HTTPException(status_code = 400, detail="The identifier is not associated with any existing database")

    
    