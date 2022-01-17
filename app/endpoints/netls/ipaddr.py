from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.errcode import *
from app.core import get_db, ok, failed, failed_errcode, get_hashcode
from app.schema.netls import IpAddrBase
from app.curd.netls import ipaddr as ip_curd


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
    _, idc = idc_curd.get(db, ipaddr.idc_id)
    if idc:
        if not ipaddr.idc_name:
            ipaddr.idc_name = idc.name

    ipaddr_dic = ipaddr.dict()
    ipaddr_dic.update({'iphash': get_hashcode(ipaddr.ipaddr)})

    done, res = ip_curd.add(db, ipaddr_dic)
