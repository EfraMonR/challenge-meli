from app.repositories.user_data_repository import UserDataRepository as udr
from app.utils.encryption import EncryptionUtils
from app.dtos.request_user_data import RequestUserData

def insert_new_user(request: RequestUserData):
    user_name = request.user_name
    encypt_password = EncryptionUtils.encrypt(request.password)
    return udr.insert_user(user_name, encypt_password)