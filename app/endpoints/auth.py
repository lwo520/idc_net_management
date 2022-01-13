# Explain：用户管理视图
from datetime import timedelta
import typing
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends

from app import config
from app.core.depts import get_db, check_jwt_token
from app.core import response
from app.core.security import create_access_token
from app.curd.auth import authenticate
from app.core import logger
from app.schema import auth_sch


router = APIRouter(prefix='/auth')


@router.post('/login', summary="用户登录认证")
async def login(
    *,
    db: Session = Depends(get_db),
    userinfo: auth_sch.User
) -> typing.Any:
    ok, errmsg = authenticate(db, userinfo.username, userinfo.password)
    if not ok:
        return response.failed(code=500, message=errmsg)
    access_token = create_access_token(
        subject=userinfo.username,
        expires_delta=timedelta(minutes=config.TOKEN_EXPIRE_TIME)
    )
    return response.ok(data={'token': access_token})


@router.post("/logout", summary="用户退出")
async def logout(token_data: typing.Union[str, typing.Any] = Depends(check_jwt_token), ):
    """
    用户退出
    :param token_data:
    :return:
    """
    logger.info(f"用户退出->用户id:{token_data.sub}")
    return response.ok(message='退出登录成功！')

