from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from app.api import dlp_controller
from app.api import token_controller
from app.api import user_controller

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
api_router.include_router(token_controller.router, tags = ["token_controller"])
api_router.include_router(user_controller.router, tags = ["user_controller"])

app.include_router(api_router)