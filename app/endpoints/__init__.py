from fastapi import APIRouter

from .netls import vendor

api_v1_router = APIRouter()
# 注册子模块路由
# api_v1_router.include_router(auth.router)
api_v1_router.include_router(vendor.router)
# api_v1_router.include_router(geo.router)
