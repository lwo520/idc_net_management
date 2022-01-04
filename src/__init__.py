# Explain: IP管理模块
# Author：Gavin
# Date：2021/11/17ss

from fastapi import FastAPI
from starlette.requests import Request

from src.common.database import engine, SessionLocal
from starlette.middleware.cors import CORSMiddleware

from src.api_route import api_v1_router
from src import config


def create_app():
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI(
        title=config.PROJECT_NAME,
        description=config.PROJ_DESCRIPTION,
        docs_url=f"{config.API_ROUTE}/docs",
        openapi_url=f"{config.API_ROUTE}/openapi.json"
    )

    # 初始化创建数据表
    initalize_db()
    # 跨域设置
    register_cors(app)
    # 注册路由
    register_router(app)
    # 请求拦截
    register_middleware(app)

    return app


def initalize_db():
    # 创建数据库模型
    from src.models import Base
    Base.metadata.create_all(bind=engine)
    # 初始化创建管理员账号
    from src.auth.rbac import initalize_super_user
    initalize_super_user(SessionLocal())


def register_cors(app: FastAPI):
    """
    支持跨域

    :param app:
    :return:
    """
    if config.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def register_router(app: FastAPI):
    """
    注册路由
    这里暂时把两个API服务写到一起，后面在拆分
    :param app:
    :return:
    """
    # 项目API
    app.include_router(
        api_v1_router,
        prefix=config.API_ROUTE  # 前缀
    )


def register_middleware(app: FastAPI):
    """
    请求响应拦截 hook
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """

    @app.middleware("http")
    async def logger_request(request: Request, call_next):
        response = await call_next(request)
        return response
