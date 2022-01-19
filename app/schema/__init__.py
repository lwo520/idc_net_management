# Schema.
import typing
from datetime import datetime as dt

from pydantic import BaseModel, validator


class LocBaseModel(BaseModel):

    @validator('*', pre=True)
    def strip_str(cls, v):
        if v and isinstance(v, str):
            return v.strip()
        return v

    @staticmethod
    def _str_ts(ts: typing.Union[int, str]) -> str:
        try:
            if isinstance(ts, str):
                ts = int(ts)
            return dt.strftime(dt.fromtimestamp(ts), '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            raise e

    @classmethod
    def from_orm(cls, qo: typing.Any) -> BaseModel:
        qo = super().from_orm(qo)

        def trans_ts_attr(keys: typing.List = None):
            for k in keys or []:
                if not hasattr(qo, k):
                    continue
                v = getattr(qo, k, 0)
                setattr(qo, k, cls._str_ts(v))
        trans_ts_attr(['created_at', 'updated_at'])

        return qo

    @classmethod
    def bm_list(cls, qo_list: typing.List) -> typing.List[BaseModel]:
        return [cls.from_orm(qo) for qo in qo_list]