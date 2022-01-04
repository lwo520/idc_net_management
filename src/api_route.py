from fastapi import APIRouter

from src import auth, network_res, geo


api_v1_router = APIRouter()
api_v1_router.include_router(auth.router)
api_v1_router.include_router(network_res.router)
api_v1_router.include_router(geo.router)
