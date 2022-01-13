import time
from sqlalchemy import Column, BIGINT
from sqlalchemy.orm import as_declarative, declared_attr


def now_ts() -> int:
    ts = int(time.time())
    return ts


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        import re
        # 如果没有指定__tablename__  则默认使用model类名转换表名字
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        if name_list[-1] == 'model':
            name_list = name_list[ :-1]
        return "_".join(name_list).lower()

    # 通用的字段
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    created_time = Column(BIGINT, default=now_ts(), comment="创建时间")
    updated_time = Column(BIGINT, default=now_ts(), onupdate=now_ts, comment="更新时间")