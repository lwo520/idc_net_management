from fastapi import APIRouter

from .netls import vendor, idc, vlanid, ipaddr

api_v1_router = APIRouter()

# 总览
api_v1_router.include_router(netls.router)
# 认证
# api_v1_router.include_router(auth.router)
# 地理信息
# api_v1_router.include_router(geo.router)
# IP管理
api_v1_router.include_router(vendor.router)
api_v1_router.include_router(idc.router)
api_v1_router.include_router(vlanid.router)
api_v1_router.include_router(ipaddr.router)
