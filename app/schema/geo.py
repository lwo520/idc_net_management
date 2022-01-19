from typing import Optional

from app.schema import LocBaseModel


class ContinentSchema(LocBaseModel):
    id: int
    cn_name: str
    en_name: str

    class Config:
        orm_mode = True


class CountrySchema(LocBaseModel):
    id: int
    name: str
    cname: str
    # continent: Continent = None
    # cities: List[Any] = []

    class Config:
        orm_mode = True


class CitySchema(LocBaseModel):
    id: int
    state: Optional[str] = None
    name: str
    cn_state: Optional[str] = None
    cn_city: str
    # country: Country = None

    class Config:
        orm_mode = True
