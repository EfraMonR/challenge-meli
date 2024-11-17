from fastapi import APIRouter
from app.dtos.request_data_base import RequestDataBase
from app.services.data_persistence_service import database_persistence
from app.services.data_clasification_service import database_clasification

router = APIRouter()

@router.post(path = "/api/v1/database", status_code = 201)
async def data_connection_persistence(request: RequestDataBase):
    return database_persistence(request)

@router.post(path = "/api/v1/database/scan", status_code = 201)
async def data_clasification(id_database):
    return database_clasification(id_database)