from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from app.dtos.request_data_base import RequestDataBase
from app.dtos.request_information_classification import RequestInformationClassification
from app.services.data_persistence_service import database_persistence
from app.services.data_clasification_service import database_clasification, get_last_scan, get_data_render, insert_information_classification

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

@router.get("/api/v1/database/view", response_class = HTMLResponse)
async def get_classification_page(request: Request, id_database: int):
    return get_data_render(request, id_database) 

@router.post(path = "/api/v1/database/addinformationtype", status_code = 201)
async def add_information_type(request: RequestInformationClassification):
    return insert_information_classification(request)