from pydantic import BaseModel


class A2ARequest(BaseModel):
    action: str
    payload: dict


class A2AResponse(BaseModel):
    status: str
    data: dict
