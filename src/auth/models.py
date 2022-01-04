from sqlalchemy import Column, String, Integer

from src.models import Base


class UserModel(Base):
    """
    用户信息model
    """
    __tablename__ = 'ty_users'

    clientid = Column(Integer, default=0, comment='Ogcloud用户ID')
    username = Column(String(64), nullable=False, unique=True, comment='用户名')
    password = Column(String(64), nullable=False, comment='用户密码，加密存储')
    is_active = Column(Integer, default=1, comment='用户是否激活，0-否，1-是')
    is_manager = Column(Integer, default=0, comment='是否为管理员，0-否，1-是')