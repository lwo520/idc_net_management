from typing import Optional, List

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class User(BaseModel):
    client_id: str
    uid: str
    username: str
    hashed_password: str
    mobile: str
    email: Optional[str] = None
    is_active: Optional[int] = 1
    is_admin: Optional[int] = 0

    class Config:
        orm_mode = True
