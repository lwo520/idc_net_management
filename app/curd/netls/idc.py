import typing

from sqlalchemy.orm import Session

from app.core import ObjectExistsError, ObjectNotFound, curd_ac_deco, update_qo
from app.models.netls import IdcModel

from ...schema.netls import Idc, IdcDetail


@curd_ac_deco
def add(db: Session, idc: typing.Dict) -> typing.Tuple[bool, typing.Any]:
    qobj = db.query(IdcModel).filter(IdcModel.name == idc['name']).first()
    if qobj:
        raise ObjectExistsError('机房【{}】已存在'.format(idc['name']))
    if idc.get('vendor_id', 0) > 0:
        if not idc.get('vendor_name'):
            from .vendor import get as vendor_get
            _, vendor = vendor_get(db, idc['vendor_id'])
            if not vendor:
                raise ObjectNotFound('供应商不存在，请检查！')
            idc.update({'vendor_name': vendor.comp_fullname})
    idc_qo = IdcModel(**idc)
    db.add(idc_qo)
    db.commit()
    db.refresh(idc_qo)
    return True, idc_qo.id


@curd_ac_deco
def delete(db: Session, id: int) -> typing.Tuple[bool, typing.Any]:
    db.query(IdcModel).filter(IdcModel.id == id).\
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def batch_delete(db: Session, id_list: typing.List[int]) -> typing.Tuple[bool, typing.Any]:
    db.query(IdcModel).filter(IdcModel.id.in_(id_list)).\
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def update(db: Session, idc: typing.Dict) -> typing.Tuple[bool, typing.Any]:
    qobj = db.query(IdcModel).filter_by(id=idc.pop('id')).first()
    if not qobj:
        raise ObjectNotFound('机房对象不存在')
    if idc.get('vendor_id', 0) > 0:
        if idc['vendor_id'] != qobj.vendor_id:
            from .vendor import get as vendor_get
            _, vendor = vendor_get(db, idc['vendor_id'])
            if not vendor:
                raise ObjectNotFound('供应商不存在，请检查！')
            idc.update({'vendor_name': vendor.comp_fullname})
    update_qo(qobj, idc)
    db.commit()
    return True, None


@curd_ac_deco
def get(db: Session, id: int) -> typing.Tuple[bool, typing.Any]:
    qobj = db.query(IdcModel).filter(IdcModel.id == id).first()
    if qobj:
        return True, IdcDetail.from_orm(qobj)
    return True, None


@curd_ac_deco
def get_list(
        db: Session, name: str, vendor_id: int,
        vendor_name: str, country: str, city: str,
        page: int = 0, page_size: int = 10
) -> typing.Tuple[bool, typing.Any]:
    qobjs = db.query(IdcModel)
    if name:
        qobjs = qobjs.filter(IdcModel.name.like(f"%{name}%"))
    if vendor_id > 0:
        qobjs = qobjs.filter(IdcModel.vendor_id == vendor_id)
    if vendor_name:
        qobjs = qobjs.filter(IdcModel.vendor_name.like(f"%{vendor_name}%"))
    if country:
        qobjs = qobjs.filter(IdcModel.country == country)
    if city:
        qobjs = qobjs.filter(IdcModel.city == city)
    if page > 0:
        offset_pos = (page - 1) * page_size
        qobjs = qobjs.offset(offset_pos).limit(page_size)
    qobjs = qobjs.all()
    return True, [Idc.from_orm(o) for o in qobjs]


@curd_ac_deco
def statistics(db: Session) -> typing.Tuple[bool, typing.Any]:
    idc_cnt = db.query(IdcModel).count()
    return True, idc_cnt
