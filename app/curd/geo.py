from typing import List
from sqlalchemy.orm import Session

from app.models.geo import CountryModel
from app.schema.geo import CountrySchema


def get_all_countries(db: Session, contient_id: int = 0) -> List[CountrySchema]:
    qobjs = db.query(CountryModel)
    if contient_id > 0:
        qobjs = qobjs.filter(CountryModel.continent_id == contient_id)
    qobjs = qobjs.group_by(CountryModel.continent_id).order_by(CountryModel.name)
    result = qobjs.all()
    return [CountrySchema.from_orm(o) for o in result]


def get_country(db: Session, cid: int):
    qobj = db.query(CountryModel).filter(CountryModel.id == cid).first()
    if qobj:
        return CountrySchema.from_orm(qobj)