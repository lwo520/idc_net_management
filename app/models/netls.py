from sqlalchemy import Column, ForeignKey, String, INT, SMALLINT, BIGINT
from sqlalchemy.orm import relationship

from app.models import Base


class VendorModel(Base):
    """
    供应商模型
    """
    __tablename__ = 'ty_vendor'

    comp_hash = Column(String(64), unique=True, index=True, comment='HASH码')
    comp_name = Column(String(32), default='', comment='公司简称')
    comp_fullname = Column(String(64), nullable=False, comment='公司全称')
    concact = Column(String(32), default='', comment='联系人')
    concact_phone = Column(String(32), default='', comment='联系电话')
    receiver = Column(String(32), default='', comment='收件人')
    recv_address = Column(String(256), default='', comment='收件地址')
    recv_phone = Column(String(32), default='', comment='收件电话')
    remarks = Column(String(256), default='', comment='备注')


class IdcModel(Base):
    """
    机房模型
    """
    __tablename__ = 'ty_idc'

    name = Column(String(64), nullable=False, comment='机房名称')
    address = Column(String(256), default='', comment='机房地址')
    concact = Column(String(32), default='', comment='联系人')
    concact_phone = Column(String(32), default='', comment='联系电话')
    country = Column(String(32), default='', comment='所属国家')
    city = Column(String(64), default='', comment='所属城市')
    vendor_id = Column(BIGINT, default=0, comment='供应商ID')
    vendor_name = Column(String(64), default='', comment='供应商公司全称')
    receiver = Column(String(32), default='', comment='收件人')
    recv_address = Column(String(256), default='', comment='收件地址')
    recv_phone = Column(String(20), default='', comment='收件电话')
    remarks = Column(String(256), default='', comment='备注')


class VlanIdModel(Base):
    """
    VlanID模型
    """
    __tablename__ = 'ty_vlanid'

    vlan_id = Column(String(6), nullable=False, comment='1-4096，以及2个特殊的：L3 和BGP')
    name = Column(String(32), default='', comment='Vlan名称')
    network = Column(String(64), default='', comment='IP网段')
    country = Column(String(32), default='', comment='所属国家')
    city = Column(String(64), default='', comment='空或某个机房所属城市')
    idc_id = Column(BIGINT, default=0, comment='机房ID')
    idc_name = Column(String(64), default='', comment='机房名称')
    remarks = Column(String(256), default='', comment='备注')


class IPModel(Base):
    """
    IP基础模型
    """
    __tablename__ = 'ty_ipaddr'

    vlan_id = Column(String(6), default='', comment='1-4096，以及2个特殊的：L3 和BGP')
    iphash = Column(String(64), index=True, comment='IP哈希码')
    ipaddr = Column(String(32), comment='IP，支持网段、IP地址、IP范围')
    flag = Column(SMALLINT, default=0, comment='IP标志，0-内网，1-公网')
    ipver = Column(SMALLINT, default=4, comment='Version，目前只支持IPv4')
    is_assigned = Column(SMALLINT, default=0, comment='是否已被使用，0-否，1-是')
    assignment = Column(String(128), default='', comment='IP分配信息')
    idc_id = Column(BIGINT, default=0, comment='机房ID')
    idc_name = Column(String(64), default='', comment='机房名称')
    ip_owner = Column(String(64), default='', comment='IP归属')
    dns = Column(String(32), default='8.8.8.8', comment='DNS')
    netmask = Column(INT, default=24, comment='子网掩码')
    remarks = Column(String(256), default='', comment='备注')


class IpExpandModel(Base):
    """
    IP扩展模型。
    """
    __tablename__ = 'ty_ipaddr_expand'

    ipaddr_id = Column(BIGINT, ForeignKey('ty_ipaddr.id'), comment='IP_ID')
    ipaddr = Column(String(32), comment='IP地址')
    flag = Column(SMALLINT, default=0, comment='IP标志，0-内网，1-公网')
    is_assigned = Column(SMALLINT, default=0, comment='是否已被使用，0-否，1-是')
    assignment = Column(String(128), default='', comment='IP分配信息')
    relate_inf = Column(String(32), default='', comment='关联网口，内网')
    idc_device = Column(String(64), default='', comment='IDC设备，公网')
    idc_dev_port = Column(String(32), default='', comment='IDC设备关联端口，公网')
