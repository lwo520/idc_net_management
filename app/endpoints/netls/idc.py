import typing

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import get_db, ok, failed, ObjectExistsError, ObjectNotFound, failed_errcode
from app.errcode import *

from app.curd.netls import idc as idc_curd
from app.schema.netls import IdcAdd, IdcUpd

router = APIRouter(prefix='/netls', tags=['IP-机房管理'])


@router.post('/idc/add', summary='添加机房')
def add_idc(
        idc: IdcAdd,
        db: Session = Depends(get_db)
):
    if not (idc.name and idc.name.strip()):
        return failed(ParamError.code, message='IDC名称不能为空值')
    try:
        done, idc_id = idc_curd.add(db, idc.dict())
        if not done:
            return failed(message='新增机房失败，请联系管理员处理！')
        return ok(data={'id': idc_id})
    except (ObjectExistsError, ObjectNotFound) as e:
        return failed(message=e.args[0])


@router.delete('/idc/', summary='删除机房')
def delete_idc(
        id: int,
        db: Session = Depends(get_db)
):
    if id <= 0:
        return failed(ParamError.code, message='Id必须大于0')
    done, _ = idc_curd.delete(db, id)
    if not done:
        return failed(message='删除机房失败')
    return ok()


@router.delete('/idc/list', summary='批量删除机房')
def delete_idcs(
        id_list: typing.List[int],
        db: Session = Depends(get_db)
):
    if not id_list:
        return failed(ParamError.code, message=ParamError.msg)
    done, _ = idc_curd.batch_delete(db, id_list)
    if not done:
        return failed(message='删除机房失败')
    return ok()


@router.put('/idc/', summary='更新机房')
def update_idc(
        idc: IdcUpd,
        db: Session = Depends(get_db)
):
    if idc.id <= 0:
        return failed_errcode(ParamError)
    done, _ = idc_curd.update(db, idc.dict())
    if not done:
        return failed(message='更新机房信息失败')
    return ok()


@router.get('/idc/', summary='获取机房详情')
def get_idc(
        id: int,
        db: Session = Depends(get_db)
):
    if id <= 0:
        return failed(ParamError.code, message='Id必须大于0')
    done, idc = idc_curd.get(db, id)
    if not done:
        return failed(message='获取机房详情失败')
    if not idc:
        return failed(NotFoundError.code, message='供应商不存在')
    return ok(data=idc)


@router.get('/idc/list/', summary='获取机房列表')
def list_idcs(
        name: str = '', vendor_id: int = 0, vendor_name: str = '',
        country: str = '', city: str = '', page: int = 0,
        page_size: int = 10, db: Session = Depends(get_db)
):
    done, idcs = idc_curd.get_list(
        db, name.strip(), vendor_id,
        vendor_name.strip(), country.strip(), city.strip(),
        page, page_size
    )
    if not done:
        return failed(message='获取机房列表失败')
    return ok(data=idcs)
