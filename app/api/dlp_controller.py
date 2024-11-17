from fastapi import APIRouter
from app.dtos.request_data_base import RequestDataBase
from app.services.data_persistence_service import database_persistence
from app.services.data_clasification_service import database_clasification, get_last_scan

router = APIRouter()

@router.post(path = "/api/v1/database", status_code = 201)
async def data_connection_persistence(request: RequestDataBase):
    return database_persistence(request)

@router.post(path = "/api/v1/database/scan", status_code = 201)
async def data_clasification(id_database):
    return database_clasification(id_database)

@router.get(path = "/api/v1/database/scan/", status_code = 201)
async def get_classification_database(id_database):
    return get_last_scan(id_database)