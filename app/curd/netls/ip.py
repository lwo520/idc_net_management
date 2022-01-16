# IP管理

import typing, ipaddress

from sqlalchemy import func
from sqlalchemy.orm.session import Session
from app.core import get_hashcode


def parse_sub_network(network: str) -> typing.Tuple[bool, typing.Any]:
    """
    处理IP子网
    """
    try:
        subnets = ipaddress.ip_network(network)
    except ValueError:
        return False, 'IP子网主机位设置错误！'
    else:
        range_ = [str(sub) for sub in subnets.hosts()]
    return True, range_


def parse_ip_range(ip_range: str) -> typing.Tuple[bool, typing.Any]:
    """
    处理IP区间
    """
    if ip_range.count('~') != 1:
        return False, 'IP段区间输入错误，正确如：192.168.0.10~100'
    st, end = ip_range.split('~')
    try:
        ipaddress.ip_address(st)
    except ValueError:
        return False, 'IP段区间输入错误，正确如：192.168.0.10~100'
    try:
        int(end)
    except ValueError:
        return False, 'IP段区间输入错误，正确如：192.168.0.10~100'
    st_sec = st.split('.')
    st_prefix, st_end = '.'.join(st_sec[: -1]), st_sec[-1]
    if int(st_end) > int(end):
        return False, 'IP段区间输入错误，起始值比结束值大'
    range_ = ['{}.{}'.format(st_prefix, x) for x in range(int(st_end), int(end) + 1)]
    return True, range_


def get(db: Session, ip: str) -> typing.Any:
    """
    # 查询IP信息
    :param db: 会话实例
    :param ip: IP地址
    """
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False, 'IP地址有错误，请检查！'
    qobj = db.query(IpInfoModel). \
        filter(IpInfoModel.ipcode == get_hashcode(ip)).first()
    if qobj:
        ipinfo = {
            'ipcode': qobj.ipcode,
            'ip': ip,
            'is_used': qobj.is_assigned,
            'clientid': qobj.clientid,
            'netmask': qobj.netmask
        }
        return True, ipinfo
    return False, '没有找到对应的IP信息！'


def get_ipinfo_list(
        db: Session, ip: str = None, is_used: int = None,
        clientid: int = 0, network: str = None, ip_range: str = None,
        page: int = 0, page_size: int = 10
) -> typing.Tuple[bool, typing.Any]:
    """
    # 查询IP信息
    :param db: 会话实例
    :param ip: IP地址，模糊查询（可选）
    :param is_used: 是否已经被使用（可选）
    :param clientid: ogcloud用户ID（可选）
    :param network: IP子网，根据IP子网查询（可选）
    :param ip_range: IP段区间，如192.168.0.10~100（可选）
    :param page: 分页页码
    :param page_size: 页容量
    """
    entities = (
        IpInfoModel.ipcode, IpInfoModel.ip, IpInfoModel.is_assigned,
        IpInfoModel.clientid, IpInfoModel.netmask
    )
    conditions = []
    if ip:
        conditions.append(IpInfoModel.ip.like(f"{ip}%"))
    if clientid is not None and clientid > 0:
        conditions.append(IpInfoModel.clientid == clientid)
    if is_used is not None:
        conditions.append(IpInfoModel.is_assigned == is_used)
    ipcode_range = []
    # 处理IP子网掩码和IP区间两种查询情况
    parse_func = parse_sub_network if network else parse_ip_range if ip_range else None
    if parse_func:
        ok, result = parse_func(network or ip_range)
        if not ok:
            return ok, result
        ipcode_range = [get_hashcode(v) for v in result]
    if ipcode_range:
        conditions.append(IpInfoModel.ipcode.in_(ipcode_range))
    qobjs = db.query(*entities).filter(*conditions)
    if page > 0:
        page_offset = (page - 1) * page_size
        qobjs = qobjs.offset(page_offset).limit(page_size)
    result = qobjs.all()
    ipinfo_list = [
        {'ipcode': o.ipcode, 'ip': o.ip, 'clientid': o.clientid,
         'is_used': o.is_assigned}
        for o in result
    ]
    # 查询数量
    total = db.query(func.count(IpInfoModel.id)).filter(*conditions).scalar()
    return True, {'total': total, 'ip_list': ipinfo_list}


def add_ipinfo_impl(
        db: Session, clientid: int = 0, ip: str = None,
        network: str = None, ip_range: str = None
) -> typing.Tuple[bool, str]:
    """
    # 新增IP信息
    :param db: 会话实例
    :param ip: IP地址，模糊查询（可选）
    :param clientid: ogcloud用户ID（可选）
    :param network: IP子网，根据IP子网查询（可选）
    :param ip_range: IP段区间，如192.168.0.10~100（可选）
    """
    if not (ip or network or ip_range):
        return False, 'IP、子网和IP段不能同时为空！'
    new_ip_list = []
    if ip:
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            return False, 'IP地址格式错误！'
        else:
            new_ip_list.append(ip)
    parse_func = parse_sub_network if network else parse_ip_range if ip_range else None
    if parse_func:
        ok, result = parse_func(network or ip_range)
        if not ok:
            return ok, result
        new_ip_list.extend(result)
    # 计算ip哈希码，并根据哈希码去重
    new_ipcode_list = [get_hashcode(ip_) for ip_ in new_ip_list]
    # 查询已存在的IP
    exists = db.query(IpInfoModel.ip). \
        filter(IpInfoModel.ipcode.in_(new_ipcode_list)).all()
    for exist in exists:
        new_ip_list.remove(exist.ip)
    new_ip_model = []
    for ip in new_ip_list:
        ipobj = {
            'ipcode': get_hashcode(ip),
            'ip': ip,
            'clientid': clientid,
        }
        new_ip_model.append(IpInfoModel(**ipobj))
    # 执行批量新增
    db.add_all(new_ip_model)
    db.commit()
    return True, 'Success'


def update_ipinfo_impl(
        db: Session, ip: str, is_used: int = None,
        clientid: int = None
):
    """
    # 更新IP信息
    :param db: 会话实例
    :param ip: IP地址列表，支持单个和多个IP
    :param clientid: ogcloud用户ID（可选）
    :param is_used: 和clienid不能同时为空（可选）
    """
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False, 'IP地址有错误，请检查！'
    if is_used is None and clientid is None:
        return False, '是否已用和ogcloud用户ID不能同时为空！'
    qobjs = db.query(IpInfoModel).filter(IpInfoModel.ipcode == get_hashcode(ip))
    if is_used is not None:
        if is_used < 0 or is_used > 1:
            return False, '是否可用的值只能为0或者1'
        qobjs.update({'is_used': is_used})
    if clientid is not None and clientid > 0:
        qobjs.update({'clientid': clientid})
    db.commit()
    return True, 'Success'


def delete_ipinfo_impl(db: Session, ip: str):
    """
    # 删除IP信息
    :param db: 会话实例
    :param ip: IP地址
    """
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False, 'IP地址有错误，请检查！'
    db.query(IpInfoModel). \
        filter(IpInfoModel.ipcode == get_hashcode(ip)).delete()
    db.commit()
    return True, 'Success'
