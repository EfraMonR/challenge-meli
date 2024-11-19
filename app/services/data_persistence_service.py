from app.dtos.request_data_base import RequestDataBase
from app.repositories.database_persistence_repository import DataBasePersistenceRepository as dbpr
from app.models.database_persistence_entity import DatabasePersistenceEntity
from app.utils.encryption import EncryptionUtils

def database_persistence(request: RequestDataBase, user_id: int):
    validation_persistence = dbpr.check_database_persistence(request)

    if(validation_persistence):
        encrypted_host = EncryptionUtils.encrypt(request.host)
        encrypted_user_name = EncryptionUtils.encrypt(request.user_name)
        encrypted_password = EncryptionUtils.encrypt(request.password)
        encrypted_port = EncryptionUtils.encrypt(request.port)

        encrypted_data = DatabasePersistenceEntity(
            host = encrypted_host,
            username = encrypted_user_name,
            password = encrypted_password,
            port = encrypted_port
        )

        id_persistence = dbpr.insert_data_persistence(encrypted_data, user_id)
        return {"The credentials of database are saved correct with id: ": f"{id_persistence}"}
    else:
        return validation_persistence


