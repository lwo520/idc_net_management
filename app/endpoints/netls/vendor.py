import typing

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.core import ok, failed, failed_errcode, get_db, ObjectExistsError
from app.errcode import *
from app.schema.netls import VendorBase, Vendor
from app.curd.netls import vendor as vendor_curd


router = APIRouter(prefix='/netls', tags=['IP-供应商管理'])


@router.post('/vendor/', summary='新增供应商')
async def add_vendor(
    vendor: VendorBase,
    db: Session = Depends(get_db)
):
    try:
        done, vendor_id = vendor_curd.add(db, vendor)
        if not done:
            return failed(message='新增供应商失败！')
        return ok(data={'id': vendor_id})
    except ObjectExistsError as e:
        return failed(message=e.args[0])


@router.delete('/vendor/', summary='删除供应商')
def delete_vendor(
        id: int,
        db: Session = Depends(get_db)
):
    if id <= 0:
        return failed(ParamError.code, message='Id必须大于0')
    done, _ = vendor_curd.delete(db, id)
    if not done:
        return failed(message='删除供应商失败')
    return ok()


@router.delete('/vendor/list', summary='批量删除供应商')
def delete_vendors(
        id_list: typing.List[int],
        db: Session = Depends(get_db)
):
    if not id_list:
        return failed(ParamError.code, message=ParamError.msg)
    done, _ = vendor_curd.batch_delete(db, id_list)
    if not done:
        return failed(message='删除供应商失败')
    return ok()


@router.put('/vendor/', summary='更新供应商')
def update_vendor(
        vendor: Vendor,
        db: Session = Depends(get_db)
):
    if vendor.id <= 0:
        return failed_errcode(ParamError)
    done, _ = vendor_curd.update(db, vendor)
    if not done:
        return failed(message='更新供应商信息失败')
    return ok()


@router.get('/vendor/', summary='获取供应商详情')
def get_vendor(
        id: int,
        db: Session = Depends(get_db)
):
    if id <= 0:
        return failed(ParamError.code, message='Id必须大于0')
    done, vendor = vendor_curd.get(db, id)
    if not done:
        return failed(message='获取供应商详情失败')
    if not vendor:
        return failed(NotFoundError.code, message='供应商不存在')
    return ok(data=vendor)


@router.get('/vendor/list/', summary='获取供应商列表')
def list_vendors(
        comp_name: str = '', comp_fullname: str = '',
        page: int = 0, page_size: int = 10,
        db: Session = Depends(get_db)
):
    done, vendors = vendor_curd.get_list(
        db,
        comp_name.strip(), comp_fullname.strip(),
        page, page_size
    )
    if not done:
        return failed(message='获取供应商列表失败')
    return ok(data=vendors)
