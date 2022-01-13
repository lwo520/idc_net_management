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

    idc_list = relationship('IdcModel', back_populates='vendor')


class IdcModel(Base):
    """
    机房模型
    """
    __tablename__ = 'ty_idc'

    name = Column(String(64), nullable=False, comment='机房名称')
    address = Column(String(256), default='', comment='机房地址')
    concact = Column(String(64), default='', comment='联系人')
    concact_phone = Column(String(32), default='', comment='联系电话')
    country = Column(String(32), default='', comment='所属国家')
    city = Column(String(64), default='', comment='所属城市')
    vendor_id = Column(BIGINT, ForeignKey('ty_vendor.id'), comment='供应商ID')
    receiver = Column(String(64), default='', comment='收件人')
    recv_address = Column(String(256), default='', comment='收件地址')
    recv_phone = Column(String(20), default='', comment='收件电话')
    remarks = Column(String(256), default='', comment='备注')

    vendor = relationship('VendorModel', back_populates='idc_list')


class VlanIdModel(Base):
    """
    VlanID模型
    """
    __tablename__ = 'ty_vlanid'

    vlan_id = Column(String(6), nullable=False, comment='1-4096，以及2个特殊的：L3 和BGP')
    name = Column(String(50), default='', comment='Vlan名称')
    network = Column(String(64), default='', comment='IP网段')
    city = Column(String(64), default='', comment='空或某个机房所属城市')
    remarks = Column(String(256), default='', comment='备注')


class IPModel(Base):
    """
    IP模型
    """
    __tablename__ = 'ty_ipaddr'

    vlan_id = Column(String(6), default='', comment='1-4096，以及2个特殊的：L3 和BGP')
    iphash = Column(String(64), unique=True, index=True, comment='IP哈希码')
    flag = Column(SMALLINT, default=0, comment='0-内网，1-公网')
    ip = Column(String(32), unique=True, comment='IP，支持网段、IP地址、IP范围')
    is_used = Column(SMALLINT, default=0, comment='是否已被使用，0-否，1-是')
    idc_device = Column(String(64), default='', comment='IDC设备')
    idc_dev_port = Column(String(32), default='', comment='IDC设备关联端口')
    relate_inf = Column(String(32), default='', comment='关联界面')
    ip_owner = Column(String(64), default='', comment='IP所有者')
    dns = Column(String(32), default='8.8.8.8', comment='DNS')
    assignment = Column(String(128), default='', comment='IP分配与作用')
    netmask = Column(INT, default=24, comment='子网掩码')
    remarks = Column(String(256), default='', comment='备注')


class IpExpandModel(Base):
    """
    IP详情模型，如果内网或者公网IP输入是网段、范围，将在这里展开。
    """
    __tablename__ = 'ty_ipaddr_expand'

    iphash = Column(String(64), ForeignKey('ty_ipaddr.iphash'), comment='IP哈希码')
    ipaddr = Column(String(32), comment='IP地址')
    is_used = Column(SMALLINT, default=0, comment='是否已被使用，0-否，1-是')
