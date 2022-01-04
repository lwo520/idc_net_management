from sqlalchemy import Column, String, Integer

from src.models import Base


class IdcManageModel(Base):
    __tablename__ = 'ty_idc'

    name = Column(String(256), nullable=False, comment='机房名称')
    address = Column(String(512), default='', comment='机房地址')
