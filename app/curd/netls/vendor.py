import typing, pinyin
from typing import Any

from sqlalchemy.orm import Session

from app.core import curd_ac_deco, get_hashcode, trans_qo_ts, upd_qo_attrs
from app.core.excepts import ObjectExistsError, ObjectNotFound
from app.models.netls import VendorModel, IdcModel
from app.schema.netls import VendorBase, Vendor, VendorDetail


@curd_ac_deco
def add(db: Session, vendor: VendorBase) -> typing.Tuple[bool, int]:
    vendor_dic = vendor.dict()

    comp_hash = get_hashcode(vendor_dic['comp_fullname'])
    vendor_dic.update({'comp_hash': comp_hash})

    if not vendor_dic['comp_name']:
        try:
            vendor_dic['comp_name'] = pinyin.get(vendor_dic['comp_fullname'])
        except:
            vendor_dic['comp_name'] = vendor_dic['comp_fullname']

    qobj = db.query(VendorModel).filter_by(comp_hash=comp_hash).first()
    if qobj:
        raise ObjectExistsError('{}对象已存在'.format(vendor_dic['comp_fullname']))

    vendor_qo = VendorModel(**vendor_dic)
    db.add(vendor_qo)
    db.commit()
    db.refresh(vendor_qo)
    return True, vendor_qo.id


@curd_ac_deco
def delete(db: Session, id: int) -> typing.Tuple[bool, Any]:
    db.query(VendorModel).filter(VendorModel.id == id).\
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def batch_delete(db: Session, id_list: typing.List[int]) -> typing.Tuple[bool, Any]:
    db.query(VendorModel).filter(VendorModel.id.in_(id_list)).\
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def update(db: Session, vendor: Vendor) -> typing.Tuple[bool, Any]:
    vendor_dic = vendor.dict()
    qobj = db.query(VendorModel).filter_by(id=vendor_dic.pop('id')).first()
    if not qobj:
        raise ObjectNotFound('供应商对象不存在')
    if vendor.comp_fullname:
        db.query(IdcModel).filter(IdcModel.vendor_id == qobj.id).\
            update({'vendor_name': vendor.comp_fullname}, synchronize_session=False)
    upd_qo_attrs(qobj, vendor)
    db.commit()
    return True, None


@curd_ac_deco
def get(db: Session, id: int) -> typing.Tuple[bool, Any]:
    qobj = db.query(VendorModel).filter(VendorModel.id == id).first()
    if qobj:
        return True, VendorDetail.from_orm(trans_qo_ts(qobj))
    return True, None


@curd_ac_deco
def get_list(db: Session, comp_name: str, comp_fullname: str,
             page: int, page_size: int) -> typing.Tuple[bool, Any]:
    qobjs = db.query(VendorModel)
    if comp_name:
        qobjs = qobjs.filter(VendorModel.comp_name.like(f"%{comp_name}%"))
    if comp_fullname:
        qobjs = qobjs.filter(VendorModel.comp_fullname.like(f"%{comp_fullname}%"))
    if page > 0:
        offset_pos = (page - 1) * page_size
        qobjs = qobjs.offset(offset_pos).limit(page_size)
    qobjs = qobjs.all()
    return True, [Vendor.from_orm(o).dict() for o in qobjs]
