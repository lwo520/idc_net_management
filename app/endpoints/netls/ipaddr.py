import ipaddress
import typing

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.enums import IPCategoryEnum
from app.errcode import *
from app.core import get_db, ok, failed, get_hashcode, ObjectExistsError, ObjectNotFound
from app.schema.netls import IPAddrAdd, IPAddr, IPAddrUpd, IPAddrExpandUpd, IPAddrQuery, IPAddrExpandQuery
from app.curd.netls import ipaddr as ip_curd


class IPValueError(ValueError):
    def __init__(self, errmsg: str = ''):
        super().__init__(errmsg)


def check_raw_ipaddr(strip_ipaddr: str) -> typing.Tuple[str, int]:
    if strip_ipaddr.count('~') == 0:
        # 非IP地址区间输入
        if strip_ipaddr.count('/') == 0:
            try:
                check = ipaddress.ip_address(strip_ipaddr)
                category = IPCategoryEnum.normal
            except ValueError:
                raise IPValueError('不合法的IPv4地址')
        elif strip_ipaddr.count('/') == 1:
            try:
                check = ipaddress.ip_network(strip_ipaddr)
                category = IPCategoryEnum.network
            except ValueError:
                raise IPValueError('不合法的IPv4网络地址')
        else:
            raise IPValueError('不合法的IP地址输入')
        if check.version != 4:
            raise IPValueError('目前只支持IPv4协议')
        return check.compressed, category
    if strip_ipaddr.count('~') == 1:
        ip_prev, ip_tail = strip_ipaddr.split('~')
        try:
            check = ipaddress.ip_address(ip_prev)
        except ValueError:
            raise IPValueError('不合法的IPv4地址: {}'.format(ip_prev))
        ip_prev_tail = int(check.compressed.split('.')[-1])
        if ip_tail.find('.') != -1:
            ip_tail = ip_tail.split('.')[-1]
        try:
            ip_tail = int(ip_tail)
        except:
            raise IPValueError('IPv4区间后缀错误，输入的不是数字')
        if ip_tail <= ip_prev_tail:
            raise IPValueError('IP段区间输入错误，起始值比结尾值大')
        # 格式化标准区间
        strip_ipaddr = '{}~{}'.format(ip_prev, ip_tail)
        return strip_ipaddr, IPCategoryEnum.iprange

    raise ValueError('IPv4地址输入有误，请检查！')


router = APIRouter(prefix='/netls', tags=['IP-IP地址管理'])


@router.post('/ipaddr/', summary='添加IP资源，支持网段和范围')
async def add_ipaddr(
        db: Session = Depends(get_db),
        *,
        ipaddr: IPAddrAdd
):
    # 检查输入的IP地址是否合法
    if not ipaddr.ipaddr.strip():
        return failed(ParamError.code, message='请输入正确的IPv4地址')
    try:
        strip_ipaddr, category = check_raw_ipaddr(ipaddr.ipaddr.strip())
    except ValueError as e:
        return failed(ParamError.code, message=e.args[0])

    ipaddr_dic = ipaddr.dict()
    ipaddr_dic.update({'ipaddr': strip_ipaddr, 'category': category})

    from app.curd.netls import idc as idc_curd
    _, idc = idc_curd.get(db, ipaddr.idc_id)
    if idc:
        if not ipaddr.idc_name or ipaddr.idc_name != idc.name:
            ipaddr_dic.update({'idc_name': idc.name})

    if ipaddr.flag == 0:
        plain_text = '0#{}'.format(ipaddr.ipaddr.strip())
        if ipaddr.vlan_id:
            plain_text = '{}#{}'.format(ipaddr.vlan_id.strip(), plain_text)
        if ipaddr.assignment:
            plain_text = '{}#{}'.format(plain_text, ipaddr.assignment.strip())
        iphash = get_hashcode(plain_text)
    else:
        iphash = get_hashcode('1#{}'.format(ipaddr.ipaddr.strip()))
    ipaddr_dic.update({'iphash': iphash})

    try:
        done, qo = ip_curd.add(db, ipaddr_dic)
        if not done:
            return failed(message='新增IP资源失败，请联系系统管理员处理')
        return ok(data={'id': qo.id})
    except (ObjectExistsError, ObjectNotFound) as e:
        return failed(message=e.args[0])


@router.delete('/ipaddr/', summary='删除IP资源')
async def delete_ipaddr(db: Session = Depends(get_db), *, id: int):
    done, _ = ip_curd.delete(db, id)
    if not done:
        return failed(message='删除IP资源失败，请联系系统管理员处理')
    return ok()


@router.delete('/ipaddr/batch/', summary='删除IP资源列表')
async def batch_del_ipaddr(db: Session = Depends(get_db), *, id_list: typing.List[int]):
    done, _ = ip_curd.delete_list(db, id_list)
    if not done:
        return failed(message='删除IP资源失败，请联系系统管理员处理')
    return ok()


@router.delete('/ipaddr/expand/', summary='删除IP网段/IP区间对应的IP地址')
async def delete_expand(db: Session = Depends(get_db), *, id: int):
    done, _ = ip_curd.delete_expand(db, id)
    if not done:
        return failed(message='删除IP地址失败，请联系系统管理员处理')
    return ok()


@router.delete('/ipaddr/expand/batch/', summary='删除IP网段/IP区间对应的IP地址列表')
async def batch_del_ipexpand(db: Session = Depends(get_db), *, id_list: typing.List[int]):
    done, _ = ip_curd.delete_exp_list(db, id_list)
    if not done:
        return failed(message='删除IP资源失败，请联系系统管理员处理')
    return ok()


async def _update(db: Session, ipaddr_dic: typing.Dict):
    try:
        done, _ = ip_curd.update(db, ipaddr_dic)
        if not done:
            return failed(message='更新IP资源失败')
        return ok()
    except (ObjectExistsError, ObjectNotFound) as e:
        return failed(message=e.args[0])


@router.put('/ipaddr/', summary='更新IP资源信息')
async def update_ipaddr(db: Session = Depends(get_db), *, ipaddr: IPAddrUpd):
    if ipaddr.id <= 0:
        return failed(ParamError.code, message='参数错误，IP资源ID不合法')
    return _update(db, ipaddr.dict())


@router.put('/ipaddr/expand/', summary='更新IP资源对应的IP地址')
async def update_ipexpand(db: Session = Depends(get_db), *, ipexpand: IPAddrExpandUpd):
    if ipexpand.id <= 0:
        return failed(ParamError.code, message='参数错误，IP地址ID不合法')
    ipaddr_dic = ipexpand.dict()
    ipaddr_dic.update({'expand': True})
    return _update(db, ipaddr_dic)


async def _update_batch(db: Session, list_: typing.List, expand: bool = False):
    done, _ = ip_curd.batch_update(db, list_, expand)
    if not done:
        return failed(message='批量更新IP资源失败')
    return ok()


@router.put('/ipaddr/batch/', summary='更新IP资源信息')
async def batch_upd_ipaddr(db: Session = Depends(get_db), *, ipaddrs: typing.List[IPAddrUpd]):
    return _update_batch(db, ipaddrs)


@router.put('/ipaddr/expand/batch/', summary='更新IP资源对应的IP地址')
async def batch_upd_ipexpand(db: Session = Depends(get_db), *, expands: typing.List[IPAddrExpandUpd]):
    return _update_batch(db, expands, True)


async def _get_detail(db: Session, id: int, expand: bool = False):
    done, ipaddr = ip_curd.get(db, id)
    if not done:
        return failed(message='获取IP资源/IP地址详情失败')
    return ok(data=ipaddr)


@router.get('/ipaddr/', summary='查询IP资源详情')
async def get_ipaddr(db: Session = Depends(get_db), *, id: int):
    return _get_detail(db, id)


@router.get('/ipaddr/expand/', summary='查询IP资源对应IP地址详情')
async def get_ipexpand(db: Session = Depends(get_db), *, id: int):
    return _get_detail(db, id, True)


@router.get('/ipaddr/list/', summary='查询IP资源列表')
async def get_ipaddr_list(db: Session = Depends(get_db), *, query: IPAddrQuery):
    done, list_ = ip_curd.get_list(db, query)
    if not done:
        return failed(message='获取IP资源列表失败')
    return ok(data=list_)


@router.get('/ipaddr/expand/list/', summary='查询IP资源对应IP地址列表')
async def get_ipexpand_list(db: Session = Depends(get_db), *, query: IPAddrExpandQuery):
    done, list_ = ip_curd.get_expand_list(db, query)
    if not done:
        return failed(message='获取IP资源对应IP地址列表失败')
    return ok(data=list_)
