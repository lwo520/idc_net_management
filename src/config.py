# Explain: 系统全局配置文件

import os, typing

DEBUG = True

# 项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 请求路径前缀
API_ROUTE = '/v1'

# 项目名称
PROJECT_NAME = 'TY—IP管理模块'
# 项目描述
PROJ_DESCRIPTION = "天耘IP管理系统，主要是管理IP的使用情况，支持对IP的增删改查，其中新增IP支持根据IP掩码和IP段的新增操作。"


# JWT验证密钥
SECRET_KEY = 'Jwtf7518dc84839'
# JWT默认过期时间，1个小时
TOKEN_EXPIRE_TIME = 3600
# 加密算法 
ALGORITHM = 'HS256'

# 数据库参数设置，目前仅支持 mysql数据库
DATABASES = {
    'default': {
        'host': '59.37.134.199',            # 数据库服务器IP
        'port': 3306,                       # 数据库端口
        'username': 'ljh',                  # 登录名
        'password': 'dCco8HSr5SyFl8c0',     # 登录密码
        'db': 'ty_cmdb',                    # 数据库名
        'encoding': 'utf8mb4',              # 数据编码
    }
}

# 跨域
BACKEND_CORS_ORIGINS: typing.List[str] = ['*']

# 初始化系统用户
SUPER_USER = {
    'username': 'admin',
    'password': 'Tytech@2022'
}
