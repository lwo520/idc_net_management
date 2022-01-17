import typing

from sqlalchemy.orm import Session


def add(db: Session, ipaddr_dic: typing.Dict) -> typing.Tuple[bool, typing.Any]:
    """
    新增IP地址
    Arguments:
        db: 数据库Session对象
        ipaddr_dic: IP地址信息字典
    Return:
        bool, IpAddrSchema
    """
    flag = ipaddr_dic.get('flag', 0)
    if flag == 0:
        pass
    return None