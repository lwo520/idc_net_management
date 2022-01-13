import typing

from fastapi import Depends, APIRouter
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import ok, failed, logger, get_db, ObjectExistsError
from app.errcode import ErrCode
from app.schema.netls import AddVendor, IntIdList, Vendor, VendorDetail
from app.curd.netls import vendor as vendor_curd


router = APIRouter(prefix='/netls', tags=['IP管理'])


@router.post('/vendor/', summary='新增供应商')
async def new_add_vendor(
    vendor: AddVendor,
    db: Session = Depends(get_db)
):
    try:
        err, vendor_id = vendor_curd.add(db, vendor)
        if not err:
            return failed(message='新增供应商失败！')
        return ok(data={'id': vendor_id})
    except ObjectExistsError as e:
        return failed(code=ErrCode.VENDOR_EXISTS.code, message=e.args[0])


@router.delete('/vendor/', summary='删除供应商')
def delete_vendor(
        id: int,
        db: Session = Depends(get_db)
):
    pass


@router.delete('/vendor/list', summary='批量删除供应商')
def delete_vendors(
        id_list: IntIdList,
        db: Session = Depends(get_db)
):
    pass


@router.put('/vendor/', summary='更新供应商')
def update_vendor(
        vendor: Vendor,
        db: Session = Depends(get_db)
):
    pass


@router.get('/vendor/', summary='获取供应商详情')
def update_vendor(
        id: int,
        db: Session = Depends(get_db)
):
    pass


@router.get('/vendor/list', summary='获取供应商列表')
def update_vendor(
        comp_name: str, comp_fullname: str,
        db: Session = Depends(get_db)
):
    pass
