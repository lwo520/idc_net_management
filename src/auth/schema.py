from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    is_active: int
    is_manager: int
