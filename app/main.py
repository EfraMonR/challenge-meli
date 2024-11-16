from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.api import dlp_controller

app = FastAPI()

origins = "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
async def root():
    """services"""
    return {"Challenge": "Meli DLP", "Version": "1.0.0"}

api_router = APIRouter()

api_router.include_router(dlp_controller.router, tags = ["dlp_controller"])

app.include_router(api_router)