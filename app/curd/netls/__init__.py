from pydantic import BaseModel
from sqlalchemy.orm import Session


class CURD:
    """
    CURD元类，考虑后期扩展
    """
    __module_cls__ = None
    __schema__ = None

    @classmethod
    def get(cls, db: Session, id: int):
        return db.query(cls.__module_cls__).filter(cls.__module_cls__.id == id).first()

    @classmethod
    def add(cls, db: Session, sch: BaseModel):
        pass
