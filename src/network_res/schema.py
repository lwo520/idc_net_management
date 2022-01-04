from pydantic import BaseModel


class InnerIpSchema(BaseModel):
    ipcode: str
    ip: str
    clientid: int
    is_used: int

    class Config:
        orm_mode = True