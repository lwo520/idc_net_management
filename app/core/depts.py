from typing import Optional, Any, Union

from fastapi import Header
from jose import jwt

from app import config
from app.core.database import SessionLocal
from app.core.excepts import TokenAuthError


def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_jwt_token(token: Optional[str] = Header(None)) -> Union[str, Any]:
    """
    解析验证 headers中为token的值 担任也可以用 Header(None, alias="Authentication") 或者 alias="X-token"
    :param token: JwtToken
    :return:
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
        # 抛出自定义异常， 然后捕获统一响应
        raise TokenAuthError("Token验证失败！")
    else:
        return payload
