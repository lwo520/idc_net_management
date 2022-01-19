import ipaddress
import typing

from sqlalchemy.orm import Session

from app.core import ObjectExistsError, curd_ac_deco, ObjectNotFound, update_qo
from app.enums import IPCategoryEnum
from app.models.netls import IPAddrModel, IPExpandModel
from app.schema.netls import IPAddrDetail, IPAddrExpandDetail, IPAddr, IPAddrExpand


@curd_ac_deco
def statistics(db: Session, flag: int = 1):
    public_cnt = db.query(IPAddrModel).filter_by(flag=flag, category=0).count()
    public_cnt += db.query(IPExpandModel).filter_by(flag=flag).count()
    return True, public_cnt


def _parse_network(network: str) -> typing.List[str]:
    """
    处理IP子网
    """
    subnets = ipaddress.ip_network(network)
    return [str(sub) for sub in subnets.hosts()]


def _parse_range(ip_range: str) -> typing.List[str]:
    """
    处理IP区间
    """
    st, end = ip_range.split('~')
    st_sec = st.split('.')
    st_prefix, st_end = '.'.join(st_sec[: -1]), st_sec[-1]
    range_ = ['{}.{}'.format(st_prefix, x) for x in range(int(st_end), int(end) + 1)]
    return range_


def add_ipaddr_expand(db: Session, exp_id: int, exp: str,
                flag: int, is_assigned: bool, parse_call: typing.Callable) -> None:
    ip_expands = parse_call(exp)
    exp_data = []
    for sub_ip in ip_expands:
        sub = {'ipaddr_id': exp_id, 'ipaddr': sub_ip, 'flag': flag}
        if is_assigned:
            # 如果整个IP网段被标记使用，则所有展开的IP都标记已分配
            sub.update({'is_assigned': is_assigned})
        exp_data.append(IPExpandModel(**sub))
    db.add_all(exp_data)


@curd_ac_deco
def add(db: Session, ipaddr_dic: typing.Dict) -> typing.Tuple[bool, typing.Any]:
    """
    新增IP地址
    Arguments:
        db: 数据库Session对象
        ipaddr_dic: IP地址信息字典
    Return:
        bool, IpAddrSchema
    """
    qobj = db.query(IPAddrModel). \
        filter(IPAddrModel.iphash == ipaddr_dic['iphash']).first()
    if qobj:
        raise ObjectExistsError('IP: {}已存在'.format(ipaddr_dic['ipaddr']))
    category = ipaddr_dic.pop('category')
    # IPaddr
    ipaddr = IPAddrModel(**ipaddr_dic)
    db.add(ipaddr)
    db.commit()
    db.refresh(ipaddr)

    # IPAddr Expand
    parse_call = _parse_network if category == IPCategoryEnum.network else \
        _parse_range if category == IPCategoryEnum.iprange else None
    if parse_call:
        add_ipaddr_expand(
            db, ipaddr.id, ipaddr_dic['ipaddr'],
            ipaddr_dic['flag'], ipaddr_dic['is_assigned'], parse_call
        )
        db.commit()

    return True, ipaddr


@curd_ac_deco
def delete(db: Session, id: int) -> typing.Tuple[bool, typing.Any]:
    db.query(IPExpandModel).filter(IPExpandModel.ipaddr_id == id). \
        delete(synchronize_session=False)
    db.query(IPAddrModel).filter(IPAddrModel.id == id).\
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def delete_list(db: Session, id_list: typing.List[int]):
    db.query(IPExpandModel).filter(IPExpandModel.ipaddr_id.in_(id_list)). \
        delete(synchronize_session=False)
    db.query(IPAddrModel).filter(IPAddrModel.id.in_(id_list)). \
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def delete_expand(db: Session, id: int):
    db.query(IPExpandModel).filter(IPExpandModel.id == id). \
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def delete_exp_list(db: Session, id_list: typing.List[int]):
    db.query(IPExpandModel).filter(IPExpandModel.id.in_(id_list)). \
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def update(db: Session, ipaddr_dic: typing.Dict, expand: bool = False):
    """
    更新IP资源
    Arguments:
        db: 数据库Session对象
        ipaddr_dic: IP地址信息字典
        expand: IP expand flag
    Return:
    """
    model_cls = IPAddrModel if not expand else IPExpandModel
    qobj = db.query(model_cls).filter(model_cls.id == ipaddr_dic['id']).first()
    if not qobj:
        raise ObjectNotFound('IP【{}】不存在'.format(ipaddr_dic['id']))
    if not expand and ipaddr_dic['is_assigned'] == 1 and \
            ipaddr_dic['is_assigned'] != qobj.is_assigned:
        db.query(IPExpandModel).filter(IPExpandModel.ipaddr_id == qobj.id).\
            update({'is_assigned': 1}, synchronize_session=False)
    update_qo(qobj, ipaddr_dic)
    db.commit()
    return True, None


@curd_ac_deco
def batch_update(db: Session, list_: typing.List, expand: bool = False):
    model_cls = IPAddrModel if not expand else IPExpandModel
    for sch in list_:
        qobj = db.query(model_cls).filter(model_cls.id == sch.id).first()
        if not qobj:
            continue
        upd_dic = sch.dict()
        upd_dic.pop('id')
        update_qo(qobj, upd_dic)
    db.commit()
    return True, None


@curd_ac_deco
def get(db: Session, id: int, expand: bool = False):
    model_cls = IPAddrModel if not expand else IPExpandModel
    qobj = db.query(model_cls).filter(model_cls.id == id).first()
    if qobj:
        sch_cls = IPAddrDetail if not expand else IPAddrExpandDetail
        return True, sch_cls.from_orm(qobj)
    return False, None


@curd_ac_deco
def get_list(
        db: Session, vlan_id: str, flag: int,
        ipaddr: str, is_assigned: int, assignment: str,
        idc_name: str, ip_owner: str, page: int,
        page_size: int
) -> typing.Tuple[bool, typing.Any]:
    """
    查询IP资源列表
    """
    conditions = []

    if vlan_id:
        conditions.append(IPAddrModel.vlan_id == vlan_id)
    if flag != -1:
        conditions.append(IPAddrModel.flag == flag)
    if is_assigned > -1:
        conditions.append(IPAddrModel.is_assigned == is_assigned)
    if ipaddr:
        conditions.append(IPAddrModel.ipaddr.like(f"%{ipaddr}%"))
    if idc_name:
        conditions.append(IPAddrModel.idc_name.like(f"%{idc_name}%"))
    if assignment:
        conditions.append(IPAddrModel.assignment.like(f"%{assignment}%"))
    if ip_owner:
        conditions.append(IPAddrModel.ip_owner == ip_owner)

    qobjs = db.query(IPAddrModel).filter(*conditions).order_by(IPAddrModel.created_at.desc())
    count = qobjs.count()
    if page > 0:
        offset_pos = (page - 1) * page_size
        qobjs = qobjs.offset(offset_pos).limit(page_size)
    result = {
        'count': count,
        'list': [IPAddr.from_orm(qo) for qo in qobjs.all()]
    }

    return True, result


@curd_ac_deco
def get_expand_list(
        db: Session, ipaddr_id: int, flag: int,
        ipaddr: str, is_assigned: int, assignment: str,
        relate_inf: str, idc_device: str, idc_dev_port: str,
        page: int, page_size: int
) -> typing.Tuple[bool, typing.Any]:
    """
    查询IP资源对应IP地址列表
    """
    conditions = [IPExpandModel.ipaddr_id == ipaddr_id]

    if flag > -1:
        conditions.append(IPExpandModel.flag == flag)
    if ipaddr:
        conditions.append(IPExpandModel.ipaddr.like(f"%{ipaddr}%"))
    if is_assigned > -1:
        conditions.append(IPExpandModel.is_assigned == is_assigned)
    if assignment:
        conditions.append(IPExpandModel.assignment.like(f"%{assignment}%"))
    if idc_device:
        conditions.append(IPExpandModel.assignment.like(f"%{idc_device}%"))
    if idc_dev_port:
        conditions.append(IPExpandModel.assignment.like(f"%{idc_dev_port}%"))
    if relate_inf:
        conditions.append(IPExpandModel.assignment.like(f"%{relate_inf}%"))

    qobjs = db.query(IPExpandModel).filter(*conditions).order_by(IPExpandModel.ipaddr_id.desc())
    count = qobjs.count()
    if page > 0:
        offset_pos = (page - 1) * page_size
        qobjs = qobjs.offset(offset_pos).limit(page_size)
    result = {
        'count': count,
        'list': [IPAddrExpand.from_orm(qo) for qo in qobjs.all()]
    }

    return True, result
