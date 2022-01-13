from sqlalchemy import Column, String, Integer

from ..models import Base


class UserModel(Base):
    """
    用户信息model
    """
    __tablename__ = 'ty_users'

    client_id = Column(Integer, default=0, comment='Ogcloud用户ID')
    uid = Column(String(64), nullable=False, unique=True, comment='用户ID')
    username = Column(String(128), nullable=False, unique=True, comment='用户名')
    mobile = Column(String(20), nullable=False, unique=True, comment='手机号')
    email = Column(String(64), nullable=True, unique=True, comment='邮箱')
    hashed_password = Column(String(256), nullable=False, comment='用户密码，加密存储')
    is_active = Column(Integer, default=1, comment='用户是否激活，0-否，1-是')
    is_admin = Column(Integer, default=0, comment='是否为管理员，0-否，1-是')