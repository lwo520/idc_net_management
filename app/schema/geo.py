from typing import Optional, List, Any

from pydantic import BaseModel


class ContinentSchema(BaseModel):
    id: int
    cn_name: str
    en_name: str

    class Config:
        orm_mode = True


class CountrySchema(BaseModel):
    id: int
    name: str
    cname: str
    # continent: Continent = None
    # cities: List[Any] = []

    class Config:
        orm_mode = True


class CitySchema(BaseModel):
    id: int
    state: Optional[str] = None
    name: str
    cn_state: Optional[str] = None
    cn_city: str
    # country: Country = None

    class Config:
        orm_mode = True
