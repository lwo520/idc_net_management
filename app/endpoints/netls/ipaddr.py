from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.errcode import *
from app.core import get_db, ok, failed, failed_errcode, get_hashcode
from app.schema.netls import IpAddrBase

router = APIRouter(prefix='/netls', tags=['IP-IP地址管理'])


@router.post('/ipaddr/', summary='添加IP地址，支持网段和范围')
def add_ipaddr(
        db: Session = Depends(get_db),
        *,
        ipaddr: IpAddrBase
):
    if not (ipaddr.ipaddr and ipaddr.ipaddr.strip()):
        return failed_errcode(ParamError)

    from app.curd.netls import idc as idc_curd
    done, idc = idc_curd.get(db, ipaddr.idc_id)
    if not (done and idc):
        return failed(ParamError.code, message='请输入正确的机房信息')
    if not ipaddr.idc_name:
        ipaddr.idc_name = idc.name

    ipaddr_dic = ipaddr.dict()

    iphash_code = get_hashcode('{}-{}-{}'.\
            format(ipaddr.idc_id, ipaddr.flag, ipaddr.ipaddr))
    ipaddr_dic.update({'iphash': iphash_code})
