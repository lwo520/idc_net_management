from typing import Optional

from pydantic import BaseModel, constr, validator


class AddVendor(BaseModel):
    comp_name: Optional[constr(max_length=32)] = ''
    comp_fullname: constr(max_length=64)
    concact: Optional[constr(max_length=32)] = ''
    concact_phone: Optional[constr(max_length=32)] = ''
    receiver: Optional[constr(max_length=32)] = ''
    recv_address: Optional[constr(max_length=256)] = ''
    recv_phone: Optional[constr(max_length=32)] = ''

    @validator('comp_fullname')
    def comp_fullname_not_null(cls, v):
        if not v:
            raise ValueError('公司全称不能为空值')
        return v


class Vendor(BaseModel):
    id: int
    comp_name: str
    comp_fullname: str
    concact: str
    concact_phone: str
    receiver: str
    recv_address: str
    recv_phone: str

    class Config:
        orm_mode = True
