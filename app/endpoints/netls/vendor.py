from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.core import ok, failed, logger, get_db
from app.schema.netls import AddVendor
from app.curd.netls import vendor as vendor_curd


router = APIRouter(prefix='/netls', tags=['IP管理'])


@router.post('/vendor/', summary='新增供应商')
async def new_add_vendor(
    vendor: AddVendor,
    db: Session = Depends(get_db)
):
    err, vendor = vendor_curd.add(db, vendor)
    if not err:
        return failed(message='新增供应商失败！')
    return ok(data=vendor.dict())
