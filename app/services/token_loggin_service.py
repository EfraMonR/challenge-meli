import jwt
import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from app.repositories.token_loggin_repository import TokenLoginRepository as tlr
from app.utils.encryption import EncryptionUtils
from dotenv import load_dotenv

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    data_user = tlr.search_data_user(username)
    if not data_user or EncryptionUtils.decrypt(data_user.password) != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    expire = datetime.now(timezone.utc) + timedelta(minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    token_payload = {
        "sub": form_data.username,
        "id_usuario": data_user.id,
        "exp": expire
    }
    token = jwt.encode(token_payload, os.getenv('SECRET_KEY'), algorithm = os.getenv('ALGORITHM'))
    return {"access_token": token, "token_type": "bearer"}

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms = [os.getenv('ALGORITHM')])
        
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(status_code = 401, detail = "Token expired")

        id_usuario = payload["id_usuario"] 
        return id_usuario
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Token decription error")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = 401, detail = "Invalid token")