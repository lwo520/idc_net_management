import typing

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.curd import geo_service
from app.core.depts import get_db

router = APIRouter(prefix='/geo', tags=['地理信息'])


@router.get('/countries/', summary='国家列表')
async def list_countries(
        db: Session = Depends(get_db),
        continent_id: int = 0
) -> typing.List:
    """
    获取国家列表
    """
    countries = geo_service.get_all_countries(db, continent_id)
    return countries


@router.get('/countries/<id:int>/', summary='国家详情')
async def country_detail(
        cid: int, db: Session = Depends(get_db)
) -> typing.List:
    """
    获取国家列表
    """
    countries = geo_service.get_country(db, cid)
    return countries
