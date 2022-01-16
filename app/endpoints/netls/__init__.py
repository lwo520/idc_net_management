from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import get_db, ok

router = APIRouter(prefix='/netls', tags=['IP-总览'])


@router.get('/', summary='资源统计')
def statistics_netls(db: Session = Depends(get_db)):
    from app.curd.netls import \
        vendor as vendor_curd, idc as idc_curd, vlanid as vlanid_curd

    _, vendor_cnt = vendor_curd.statistics(db)
    _, idc_cnt = idc_curd.statistics(db)
    _, vlanid_cnt = vlanid_curd.statistics(db)

    statistics = {
        'vendor': vendor_cnt or 0,
        'idc': idc_cnt or 0,
        'vlanid_cnt': vlanid_cnt or 0
    }

    return ok(data=statistics)
