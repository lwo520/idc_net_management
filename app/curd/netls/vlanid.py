import typing

from sqlalchemy.orm import Session

from app.core import ObjectExistsError, ObjectNotFound, curd_ac_deco, trans_qo_ts, upd_qo_attrs
from app.models.netls import VlanIdModel
from app.schema.netls import VlanIDDetail, VlanID


@curd_ac_deco
def add(db: Session, vlanid: typing.Dict) -> typing.Tuple[bool, typing.Any]:
    qobj = db.query(VlanIdModel).filter(VlanIdModel.vlan_id == vlanid['vlan_id']).first()
    if qobj:
        raise ObjectExistsError('VlanID【{}】已存在'.format(vlanid['name']))
    if not vlanid.get('name'):
        vlanid['name'] = 'Vlan-{}'.format(vlanid['vlan_id'])
    vlanid_qo = VlanIdModel(**vlanid)
    db.add(vlanid_qo)
    db.commit()
    db.refresh(vlanid_qo)
    return True, vlanid_qo.id


@curd_ac_deco
def delete(db: Session, id: int) -> typing.Tuple[bool, typing.Any]:
    db.query(VlanIdModel).filter(VlanIdModel.id == id).\
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def batch_delete(db: Session, id_list: typing.List[int]) -> typing.Tuple[bool, typing.Any]:
    db.query(VlanIdModel).filter(VlanIdModel.id.in_(id_list)).\
        delete(synchronize_session=False)
    db.commit()
    return True, None


@curd_ac_deco
def update(db: Session, vlanid: typing.Dict) -> typing.Tuple[bool, typing.Any]:
    qobj = db.query(VlanIdModel).filter_by(id=vlanid.pop('id')).first()
    if not qobj:
        raise ObjectNotFound('VlanID对象不存在')
    upd_qo_attrs(qobj, vlanid)
    db.commit()
    return True, None


@curd_ac_deco
def get(db: Session, id: int) -> typing.Tuple[bool, typing.Any]:
    qobj = db.query(VlanIdModel).filter(VlanIdModel.id == id).first()
    if qobj:
        return True, VlanIDDetail.from_orm(trans_qo_ts(qobj))
    return True, None


@curd_ac_deco
def get_list(
        db: Session, vlan_id: str, name: str,
        network: str, country: str, city: str,
        page: int = 0, page_size: int = 10
) -> typing.Tuple[bool, typing.Any]:
    qobjs = db.query(VlanIdModel)
    if vlan_id:
        qobjs = qobjs.filter(VlanIdModel.vlan_id == vlan_id)
    if name:
        qobjs = qobjs.filter(VlanIdModel.name.like(f"%{name}%"))
    if network:
        qobjs = qobjs.filter(VlanIdModel.network.like(f"{network}%"))
    if country:
        qobjs = qobjs.filter(VlanIdModel.country == country)
    if city:
        qobjs = qobjs.filter(VlanIdModel.city == city)
    if page > 0:
        offset_pos = (page - 1) * page_size
        qobjs = qobjs.offset(offset_pos).limit(page_size)
    qobjs = qobjs.all()
    return True, [VlanID.from_orm(o).dict() for o in qobjs]
