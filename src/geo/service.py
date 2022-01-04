from fastapi import Depends

from ..common.depts import get_db
from .models import ContinentModel, CountyModel, CityModel
from .schema import ContinentSchema, CountrySchema, CitySchema


class GeoService(object):
    """
    GEO服务实现
    """
    db = Depends(get_db)

    @classmethod
    def continent_list(cls):
        continents = cls.db.query(ContinentModel).all()
        return ContinentSchema.from_orm(continents)

