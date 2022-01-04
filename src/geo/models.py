from sqlalchemy import Column, String, Integer, SmallInteger, Text

from src.models import Base


class ContinentModel(Base):
    """
    全球七大洲model
    """
    __tablename__ = 'ty_continent'

    cn_name = Column(String(16), nullable=False, comment='洲中文名称')
    en_name = Column(String(16), nullable=False, comment='洲英文名称')


class CountyModel(Base):
    """
    全球国家信息
    """
    __tablename__ = 'ty_country'

    continent_id = Column(SmallInteger, default=0, comment='国家所在的七大洲对应的id')
    name = Column(String(256), nullable=False, comment='国家英文常用标准名称')
    lower_name = Column(String(256), default='', comment='国家英文标准名称的小写，主要用于搜索与比较')
    country_code = Column(String(256), default='', comment='国家英文代码,国家名称缩写')
    full_name = Column(String(256), default='', comment='国家英文名称全称')
    cname = Column(String(256), default='', comment='国家中文常用标准名称')
    full_cname = Column(String(256), default='', comment='国家中文名称全称')
    remark = Column(Text(4096), default='', comment='备注，国家的一些说明')
    fb_country_code = Column(String(256), default='', comment='')
    lang = Column(String(16), default='', comment='国家官方语言')


class CityModel(Base):
    """
    全球城市信息
    """
    __tablename__ = 'ty_city'

    country_id = Column(SmallInteger, default=0, comment='国家id')
    state = Column(String(256), default='', comment='城市所在的州或省')
    name = Column(String(256), nullable=False, comment='城市标准名称')
    lower_name = Column(String(256), default='', comment='城市标准名称的小写，主要用于搜索与比较')
    cn_state = Column(String(256), default='', comment='州或省的中文名称')
    cn_city = Column(String(256), default='', comment='城市的中文名称')
    city_code = Column(String(64), default='', comment='城市代码')
    family_income = Column(Integer, default=0, comment='城市GDP（美元）')
    stat_code = Column(String(64), default='', comment='州或省的代码')
