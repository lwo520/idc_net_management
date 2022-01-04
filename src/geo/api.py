import typing

from . import router
from src.geo.service import GeoService


@router.get('/')
async def continents() -> typing.List:
    return GeoService.continent_list()
