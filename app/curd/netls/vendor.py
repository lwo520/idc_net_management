import typing
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.core import curd_deco, get_hashcode
from app.core.excepts import ObjectExistsError
from app.models.netls import VendorModel
from app.schema.netls import AddVendor, Vendor


@curd_deco
def add(db: Session, vendor: AddVendor) -> typing.Tuple[bool, Vendor]:
    vendor_dic = vendor.dict()

    comp_hash = get_hashcode(vendor_dic['comp_fullname'])
    vendor_dic.update({'comp_hash': comp_hash})

    qobj = db.query(VendorModel).filter_by(comp_hash=comp_hash).first()
    if qobj:
        raise ObjectExistsError('{}对象已存在'.format(vendor_dic['comp_fullname']))

    vendor_qo = VendorModel(**vendor_dic)
    db.add(vendor_qo)
    db.commit()
    db.refresh(vendor_qo)
    return True, Vendor.from_orm(vendor_qo)
