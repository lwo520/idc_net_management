from typing import Optional

from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends

from src.common import response
from src.common.depts import get_db
from src.network_res import inner

from src.common.log import logger


router = APIRouter()


@router.get('/ip/detail', summary='查询IP详情')
async def get_ipinfo(db: Session = Depends(get_db), *, ip: str):
    """
    # 查询IP信息
    :param db: 会话实例
    :param ip: IP地址
    :return:
    """
    ok, result = service.get_ipinfo(db, ip)
    if not ok:
        return response.failed(message=result)
    return response.ok(data=result)


@router.get('/ip/list', summary='查询IP信息')
async def get_ipinfo_list(
        db: Session = Depends(get_db),
        *,
        clientid: Optional[int] = 0,
        ip: Optional[str] = None,
        is_used: Optional[int] = None,
        network: Optional[str] = None,
        ip_range: Optional[str] = None,
        page: Optional[int] = 0,
        page_size: Optional[int] = 10
):
    """
    # 查询IP信息
    :param db: 会话实例
    :param ip: IP地址，模糊查询（可选）
    :param is_used: 是否已经被使用（可选）
    :param clientid: ogcloud用户ID（可选）
    :param network: IP子网，根据IP子网查询（可选）
    :param ip_range: IP段区间，如192.168.0.10~100（可选）
    :param page: 页码（可选）
    :param page_size: 页容量（可选）
    :return:
    """
    ok, result = service.get_ipinfo_list(
        db, ip, is_used,
        clientid, network, ip_range,
        page, page_size
    )
    if not ok:
        return response.failed(message=result)
    return response.ok(data=result)


@router.post('/ip/add', summary='新增IP信息')
async def add_ipinfo(
        db: Session = Depends(get_db), *, clientid: Optional[int] = 0,
        ip: Optional[str] = None, network: Optional[str] = None, ip_range: Optional[str] = None
):
    """
    # 新增IP信息
    :param db: 会话实例
    :param ip: IP地址（可选），IP、IP子网和IP段不能同时为空
    :param clientid: ogcloud用户ID（可选）
    :param network: IP子网，根据IP子网查询（可选）
    :param ip_range: IP段区间，如192.168.0.10~100（可选）
    """
    try:
        ok, errmsg = service.add_ipinfo_impl(
            db, clientid, ip,
            network, ip_range
        )
        if not ok:
            return response.failed(message=errmsg)
        return response.ok()
    except Exception as e:
        logger.error('{}'.format(e.args[0]))
        db.rollback()
        db.delete()
        return response.failed()


@router.put('/ip/update', summary='更新IP信息')
async def update_ipinfo(
        db: Session = Depends(get_db), *, ip: str,
        is_used: Optional[int] = None, clientid: Optional[int] = None
):
    """
    # 更新IP信息
    :param db: 会话实例
    :param ip: IP地址
    :param clientid: ogcloud用户ID（可选）
    :param is_used: 和clienid不能同时为空（可选）
    """
    try:
        ok, errmsg = service.update_ipinfo_impl(db, ip, is_used, clientid)
    except Exception as e:
        logger.error('{}'.format(e.args[0]))
        db.rollback()
        db.delete()
        return response.failed()
    else:
        if not ok:
            return response.failed(message=errmsg)
        return response.ok()


@router.delete('/ip/delete', summary='删除IP信息')
async def delete_ipinfo(db: Session = Depends(get_db), *, ip: str):
    """
    # 删除IP信息
    :param db: 会话实例
    :param ip: IP地址列表，支持单个和多个IP
    """
    try:
        ok, errmsg = service.delete_ipinfo_impl(db, ip)
    except Exception as e:
        logger.error('{}'.format(e.args[0]))
        db.rollback()
        db.delete()
        return response.failed()
    else:
        if not ok:
            return response.failed(message=errmsg)
        return response.ok()