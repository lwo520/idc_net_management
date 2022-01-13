from typing import Optional

from pydantic import BaseModel, constr


class AddVendor(BaseModel):
    comp_name: Optional[constr(max_length=32)] = ''
    comp_fullname: constr(max_length=64)
    concact: Optional[constr(max_length=32)] = ''
    concact_phone: Optional[constr(max_length=32)] = ''
    receiver: Optional[constr(max_length=32)] = ''
    recv_address: Optional[constr(max_length=256)] = ''
    recv_phone: Optional[constr(max_length=32)] = ''


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
