from pydantic import BaseModel

class RequestInformationClassification(BaseModel):
    information_type: str
    information_expression: str