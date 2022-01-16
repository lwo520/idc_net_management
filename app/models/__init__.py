import time
from sqlalchemy import Column, BIGINT, String
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
    created_by = Column(BIGINT, default=0, comment='创建者ID，Ogcloud用户ID')
    created_at = Column(BIGINT, default=now_ts(), comment="创建时间")
    updated_by = Column(BIGINT, default=0, comment='更新者ID，Ogcloud用户ID')
    updated_at = Column(BIGINT, default=now_ts(), onupdate=now_ts, comment="更新时间")
