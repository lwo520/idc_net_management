from pydantic import BaseModel


class ContinentSchema(BaseModel):
    id: int
    cn_name: str
    en_name: str

    class Config:
        orm_mode = True


class CountrySchema(BaseModel):
    id: int
    continent_id: int
    name: str
    cname: str

    class Config:
        orm_mode = True


class CitySchema(BaseModel):
    id: int
    state: str
    name: str
    cn_state: str
    cn_city: str

    class Config:
        orm_mode = True
