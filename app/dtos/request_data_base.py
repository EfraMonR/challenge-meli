from pydantic import BaseModel

class RequestDataBase(BaseModel):
    host: str
    port: str
    user_name: str
    password: str