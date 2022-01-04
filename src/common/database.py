# Explain: 使用SqlAlchemy连接数据库
# Author: Gavin

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from src import config


def generate_database_url(label: str = 'default') -> str:
    """
    # 读取配置里的数据库配置，生成数据库连接
    :param label: 数据库配置标签，默认为default
    :return: str
    """
    if not hasattr(config, 'DATABASES'):
        raise AttributeError('你还没有配置数据库信息，请先配置！')
    databse_url = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8&auth_plugin=mysql_native_password'
    dbconfig = config.DATABASES.get(label)
    if not dbconfig:
        raise ValueError('没有该【{}】配置信息'.format(label))
    host, port, username, password, dbname = dbconfig['host'], dbconfig['port'], dbconfig['username'], \
                                             dbconfig['password'], dbconfig['db']
    return databse_url.format(username, password, host, port, dbname)


# 创建数据库引擎
SQLALCHEMY_DATABASE_URL = generate_database_url('default')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 元数据绑定数据库
Metadata = MetaData(bind=engine)

# 将重写Base，增加默认字段
# Base = declarative_base()
