from typing import Optional, List, Any

from pydantic import BaseModel, validator, Field


class VendorBase(BaseModel):
    comp_name: Optional[str] = Field(
        default='', max_length=32, description='公司名称（简称）'
    )
    comp_fullname: Optional[str] = Field(
        max_length=64, description='公司全称，不能为空值'
    )
    concact: Optional[str] = Field(
        default='', max_length=32, description='联系人'
    )
    concact_phone: Optional[str] = Field(
        default='', max_length=32, description='联系电话'
    )
    receiver: Optional[str] = Field(
        default='', max_length=32, description='收件人'
    )
    recv_address: Optional[str] = Field(
        default='', max_length=256, description='收件地址'
    )
    recv_phone: Optional[str] = Field(
        default='', max_length=32, description='收件电话'
    )
    remarks: Optional[str] = Field(
        default='', max_length=256, description='备注'
    )

    @validator('comp_fullname')
    def comp_fullname_not_null(cls, v):
        if not v:
            raise ValueError('公司全称不能为空值')
        return v


class Vendor(BaseModel):
    id: Optional[int] = Field(description='供应商ID')
    comp_name: Optional[str] = Field(
        default='', max_length=32, description='公司名称（简称）'
    )
    comp_fullname: Optional[str] = Field(
        max_length=64, description='公司全称，不能为空值'
    )
    concact: Optional[str] = Field(
        default='', max_length=32, description='联系人'
    )
    concact_phone: Optional[str] = Field(
        default='', max_length=32, description='联系电话'
    )
    receiver: Optional[str] = Field(
        default='', max_length=32, description='收件人'
    )
    recv_address: Optional[str] = Field(
        default='', max_length=256, description='收件地址'
    )
    recv_phone: Optional[str] = Field(
        default='', max_length=32, description='收件电话'
    )

    class Config:
        orm_mode = True


class VendorDetail(VendorBase):
    id: Optional[int] = Field(description='供应商ID')
    created_time: Optional[str] = Field(default='', description='创建时间')
    idc_list: Optional[List[Any]] = Field(
        default=[], description='供应商ID列表'
    )

    class Config:
        orm_mode = True


class IdcBase(BaseModel):
    name: str = Field(
        max_length=64, description='机房名称'
    )
    address: Optional[str] = Field(
        default='', max_length=256, description='机房地址'
    )
    concact: Optional[str] = Field(
        default='', max_length=32, description='联系人'
    )
    concact_phone: Optional[str] = Field(
        default='', max_length=32, description='联系电话'
    )
    country: Optional[str] = Field(
        default='', max_length=32, description='所属国家'
    )
    city: Optional[str] = Field(
        default='', max_length=64, description='所属城市'
    )
    vendor_id: Optional[int] = Field(
        default=0, description='供应商ID，0表示没有关联供应商'
    )
    receiver: Optional[str] = Field(
        default='', max_length=32, description='收件人'
    )
    recv_address: Optional[str] = Field(
        default='', max_length=256, description='收件地址'
    )
    recv_phone: Optional[str] = Field(
        default='', max_length=32, description='收件电话'
    )
    remarks: Optional[str] = Field(
        default='', max_length=256, description='备注'
    )


class IdcUpd(IdcBase):
    id: Optional[int] = Field(description='机房ID')


class Idc(BaseModel):
    id: Optional[int] = Field(description='机房ID')
    name: str = Field(
        max_length=64, description='机房名称'
    )
    address: Optional[str] = Field(
        default='', max_length=256, description='机房地址'
    )
    concact: Optional[str] = Field(
        default='', max_length=32, description='联系人'
    )
    concact_phone: Optional[str] = Field(
        default='', max_length=32, description='联系电话'
    )
    city: Optional[str] = Field(
        default='', max_length=64, description='所属城市'
    )
    vendor_name: Optional[str] = Field(
        default='', max_length=64, description='供应商公司全名'
    )

    class Config:
        orm_mode = True


class IdcDetail(IdcUpd):
    vendor_name: Optional[str] = Field(
        default='', max_length=64, description='供应商公司全名'
    )
    created_time: Optional[str] = Field(default='', description='创建时间')

    class Config:
        orm_mode = True


class VlanIDBase(BaseModel):
    vlan_id: str = Field(
        max_length=6, description='数字1-4096，以及2个特殊的：L3 和BGP'
    )
    name: Optional[str] = Field(
        default='', max_length=32, description='Vlan名称'
    )
    network: Optional[str] = Field(
        default='', max_length=64, description='IP网段'
    )
    country: Optional[str] = Field(
        default='', max_length=32, description='所属国家'
    )
    city: Optional[str] = Field(
        default='', max_length=64, description='空或某个机房所属城市'
    )
    remarks: Optional[str] = Field(
        default='', max_length=256, description='备注'
    )


class VlanID(BaseModel):
    id: Optional[int] = Field(description='ID')
    vlan_id: Optional[str] = Field(
        default='', max_length=6, description='数字1-4096，以及2个特殊的：L3 和BGP'
    )
    name: Optional[str] = Field(
        default='', max_length=32, description='Vlan名称'
    )
    network: Optional[str] = Field(
        default='', max_length=64, description='IP网段'
    )
    country: Optional[str] = Field(
        default='', max_length=32, description='所属国家'
    )
    city: Optional[str] = Field(
        default='', max_length=64, description='空或某个机房所属城市'
    )

    class Config:
        orm_mode = True


class VlanIDDetail(VlanIDBase):
    id: Optional[int] = Field(description='ID')
    created_time: Optional[str] = Field(default='', description='创建时间')

    class Config:
        orm_mode = True
