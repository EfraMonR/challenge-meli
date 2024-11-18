from fastapi import APIRouter
from app.services.user_data_service import insert_new_user
from app.dtos.request_user_data import RequestUserData

router = APIRouter()

@router.post(path = "/api/v1/addUser", status_code = 201)
async def add_user(request: RequestUserData):
    return insert_new_user(request)