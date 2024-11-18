from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.token_loggin_service import login

router = APIRouter()

@router.post(path = "/api/v1/token", status_code = 201)
async def login_api(form_data: OAuth2PasswordRequestForm = Depends()):
    return login(form_data)