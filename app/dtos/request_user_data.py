from pydantic import BaseModel

class RequestUserData(BaseModel):
    user_name: str
    password: str