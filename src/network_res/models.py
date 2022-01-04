from sqlalchemy import Column, String, Integer

from src.models import Base


class InnerManageModel(Base):
    """
    内网管理模型
    """
    __tablename__ = 'ty_intranet'

    ipcode = Column(String(64), unique=True, index=True, comment='IP对应的哈希码')
    ip = Column(String(20), unique=True, comment='IP')
    clientid = Column(Integer, default=0, comment='ogcloud用户ID')
    is_used = Column(Integer, default=0, comment='是否已被使用，0-否，1-是')
    netmask = Column(Integer, default=24, comment='子网掩码')