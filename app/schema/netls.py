import typing
from typing import Optional, List, Any
from datetime import datetime as dt

from pydantic import BaseModel, validator, Field

from app.enums import NetFlagEnum


class IPBase(BaseModel):
    @staticmethod
    def _str_ts(ts: typing.Union[int, str]) -> str:
        try:
            if isinstance(ts, str):
                ts = int(ts)
            return dt.strftime(dt.fromtimestamp(ts), '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            raise e

    @classmethod
    def from_orm(cls, qo: typing.Any) -> BaseModel:
        qo = super().from_orm(qo)

        def trans_ts_attr(keys: typing.List = None):
            for k in keys or []:
                if not hasattr(qo, k):
                    continue
                v = getattr(qo, k, 0)
                setattr(qo, k, cls._str_ts(v))
        trans_ts_attr(['created_at', 'updated_at'])

        return qo

    @classmethod
    def bm_list(cls, qo_list: typing.List) -> typing.List[BaseModel]:
        return [cls.from_orm(qo) for qo in qo_list]


class VendorBase(IPBase):
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
    created_by: Optional[str] = Field(
        default='', max_length=64, description='创建者，非本地用户信息，故显示名称'
    )
    remarks: Optional[str] = Field(
        default='', max_length=256, description='备注'
    )

    @validator('comp_fullname')
    def comp_fullname_not_null(cls, v):
        if not v:
            raise ValueError('公司全称不能为空值')
        return v


class Vendor(IPBase):
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
    updated_by: Optional[str] = Field(
        default='', max_length=64, description='更新者，非本地用户信息，故显示名称'
    )

    class Config:
        orm_mode = True


class VendorDetail(VendorBase):
    id: Optional[int] = Field(description='供应商ID')
    created_by: Optional[str] = Field(default=0, description='Ogcloud用户ID')
    created_at: Optional[str] = Field(default='', description='创建时间')
    updated_by: Optional[int] = Field(default=0, description='Ogcloud用户ID')
    updated_at: Optional[str] = Field(default='', description='更新时间')

    idc_list: Optional[List[Any]] = Field(
        default=[], description='供应商ID列表'
    )

    class Config:
        orm_mode = True


class IdcBase(IPBase):
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
    created_by: Optional[str] = Field(
        default='', max_length=64, description='创建者，非本地用户信息，故显示名称'
    )
    remarks: Optional[str] = Field(
        default='', max_length=256, description='备注'
    )


class IdcUpd(IdcBase):
    id: int = Field(description='机房ID')


class Idc(IPBase):
    id: int = Field(description='机房ID')
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
    created_by: Optional[str] = Field(default=0, description='Ogcloud用户ID')
    created_at: Optional[str] = Field(default='', description='创建时间')
    updated_by: Optional[int] = Field(default=0, description='Ogcloud用户ID')
    updated_at: Optional[str] = Field(default='', description='更新时间')

    class Config:
        orm_mode = True


class VlanIDBase(IPBase):
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
    # idc_id: Optional[int] = Field(
    #     default=0, description='所属机房的ID，0表示没有关联任何机房'
    # )
    # id_name: Optional[str] = Field(
    #     default='', max_length=64, description='所属机房名称'
    # )
    created_by: Optional[str] = Field(
        default='', max_length=64, description='创建者，非本地用户信息，故显示名称'
    )
    remarks: Optional[str] = Field(
        default='', max_length=256, description='备注'
    )


class VlanID(IPBase):
    id: int = Field(description='ID')
    vlan_id: Optional[str] = Field(
        default='', max_length=6, description='数字1-4096，以及2个特殊的：L3 和BGP'
    )
    name: Optional[str] = Field(
        default='', max_length=32, description='Vlan名称'
    )
    network: Optional[str] = Field(
        default='', max_length=64, description='IP网段'
    )
    city: Optional[str] = Field(
        default='', max_length=64, description='空或某个机房所属城市'
    )
    # id_name: Optional[str] = Field(
    #     default='', max_length=64, description='所属机房名称'
    # )

    class Config:
        orm_mode = True


class VlanIDDetail(VlanIDBase):
    id: Optional[int] = Field(description='ID')
    created_by: Optional[str] = Field(default=0, description='Ogcloud用户ID')
    created_at: Optional[str] = Field(default='', description='创建时间')
    updated_by: Optional[int] = Field(default=0, description='Ogcloud用户ID')
    updated_at: Optional[str] = Field(default='', description='更新时间')

    class Config:
        orm_mode = True


class IpAddrBase(IPBase):
    vlan_id: Optional[str] = Field(
        default='', max_length=6, description='数字1-4096，以及2个特殊的：L3 和BGP'
    )
    flag: Optional[int] = Field(
        default=NetFlagEnum.inner, description='网络标志，0-内网，1-公网'
    )
    ipaddr: Optional[str] = Field(
        max_length=32, description='IP，支持网段、IP地址、IP范围'
    )
    is_assigned: Optional[int] = Field(
        default=0, description='是否已分配使用，0-否，1-是'
    )
    assignment: Optional[str] = Field(
        default='', max_length=128, description='IP分配信息'
    )
    idc_id: Optional[int] = Field(default=0, description='所属机房ID')
    idc_name: Optional[str] = Field(
        default='', max_length=64, description='所属机房名称'
    )
    idc_device: Optional[str] = Field(
        default='', max_length=64, description='IDC设备'
    )
    idc_dev_port: Optional[str] = Field(
        default='', max_length=32, description='IDC设备关联端口'
    )
    relate_inf: Optional[str] = Field(
        default='', max_length=32, description='关联界面'
    )
    ip_owner: Optional[str] = Field(
        default='', max_length=64, description='IP所有者'
    )
    dns: Optional[str] = Field(
        default='8.8.8.8', max_length=32, description='DNS'
    )
    remarks: Optional[str] = Field(
        default='', max_length=256, description='备注'
    )


class IpAddrDetail(IpAddrBase):
    id: Optional[int] = Field(description='ID')

    ipver: Optional[int] = Field(default=4, description='IP版本')
    netmask: Optional[int] = Field(default=24, description='子网掩码')

    created_by: Optional[str] = Field(default=0, description='Ogcloud用户ID')
    created_at: Optional[str] = Field(default='', description='创建时间')
    updated_by: Optional[int] = Field(default=0, description='Ogcloud用户ID')
    updated_at: Optional[str] = Field(default='', description='更新时间')


    class Config:
        orm_mode = True


class IpAddr(BaseModel):
    vlan_id: Optional[str] = Field(
        default='', max_length=6, description='数字1-4096，以及2个特殊的：L3 和BGP'
    )
    flag: Optional[int] = Field(
        default=NetFlagEnum.inner, description='网络标志，0-内网，1-公网'
    )
    ipaddr: Optional[str] = Field(
        max_length=32, description='IP，支持网段、IP地址、IP范围'
    )
    is_assigned: Optional[int] = Field(
        default=0, description='是否已分配使用，0-否，1-是'
    )
    assignment: Optional[str] = Field(
        default='', max_length=128, description='IP分配信息'
    )
    idc_name: Optional[str] = Field(
        default='', max_length=64, description='所属机房名称'
    )
    idc_device: Optional[str] = Field(
        default='', max_length=64, description='IDC设备'
    )
    idc_dev_port: Optional[str] = Field(
        default='', max_length=32, description='IDC设备关联端口'
    )
    relate_inf: Optional[str] = Field(
        default='', max_length=32, description='关联界面'
    )
    ip_owner: Optional[str] = Field(
        default='', max_length=64, description='IP所有者'
    )
    dns: Optional[str] = Field(
        default='8.8.8.8', max_length=32, description='DNS'
    )

    class Config:
        orm_mode = True


class IpAddrUpd(IpAddrBase):
    id: int = Field(description='')
