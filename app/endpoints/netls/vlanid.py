import re
import typing

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import get_db, ok, failed, ObjectExistsError, ObjectNotFound, failed_errcode
from app.errcode import *
from app.schema.netls import VlanidAdd, VlanID
from app.curd.netls import vlanid as vlanid_curd

router = APIRouter(prefix='/netls', tags=['IP-VlanID'])


@router.post('/vlanid/add', summary='添加VlanID')
async def add_vlanid(
        vlanid: VlanidAdd,
        db: Session = Depends(get_db)
):
    if not (vlanid.vlan_id and vlanid.vlan_id.strip()):
        return failed(ParamError.code, message='VlanID不能为空值')
    if vlanid.network:
        m = re.match('\d+.\d+.\d+.\d+\/\d+', vlanid.network.strip())
        if not (m and m.group(0)):
            return failed(ParamError.code, message='IP网段的格式不对，类似于：192.168.1.0/24')
    try:
        done, vlanid_id = vlanid_curd.add(db, vlanid.dict())
        if not done:
            return failed(message='新增VlanID失败，请联系管理员处理！')
        return ok(data={'id': vlanid_id})
    except (ObjectExistsError, ObjectNotFound) as e:
        return failed(message=e.args[0])


@router.delete('/vlanid/', summary='删除VlanID')
async def delete_vlanid(
        id: int,
        db: Session = Depends(get_db)
):
    if id <= 0:
        return failed(ParamError.code, message='Id必须大于0')
    done, _ = vlanid_curd.delete(db, id)
    if not done:
        return failed(message='删除VlanID失败')
    return ok()


@router.delete('/vlanid/list', summary='批量删除VlanID')
async def delete_vlanids(
        id_list: typing.List[int],
        db: Session = Depends(get_db)
):
    if not id_list:
        return failed(ParamError.code, message=ParamError.msg)
    done, _ = vlanid_curd.batch_delete(db, id_list)
    if not done:
        return failed(message='删除VlanID失败')
    return ok()


@router.put('/vlanid/', summary='更新VlanID')
async def update_vlanid(
        vlanid: VlanID,
        db: Session = Depends(get_db)
):
    if vlanid.id <= 0:
        return failed_errcode(ParamError)
    done, _ = vlanid_curd.update(db, vlanid.dict())
    if not done:
        return failed(message='更新VlanID信息失败')
    return ok()


@router.get('/vlanid/', summary='获取VlanID详情')
async def get_vlanid(
        id: int,
        db: Session = Depends(get_db)
):
    if id <= 0:
        return failed(ParamError.code, message='Id必须大于0')
    done, vlanid = vlanid_curd.get(db, id)
    if not done:
        return failed(message='获取VlanID详情失败')
    if not vlanid:
        return failed(NotFoundError.code, message='VlanID不存在')
    return ok(data=vlanid)


@router.get('/vlanid/list/', summary='获取VlanID列表')
async def list_vlanids(
        vlan_id: str = '', name: str = '', network: str = '',
        country: str = '', city: str = '',
        page: int = 0, page_size: int = 10,
        db: Session = Depends(get_db)
):
    done, vlanids = vlanid_curd.get_list(
        db, vlan_id.strip(),
        name.strip(), network.strip(),
        country.strip(), city.strip(),
        page, page_size
    )
    if not done:
        return failed(message='获取VlanID列表失败')
    return ok(data=vlanids)
