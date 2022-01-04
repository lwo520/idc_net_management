from datetime import datetime, timedelta
from typing import Any, Union

import hashlib

from jose import jwt

from src import config


def encrypt_plaintext_md5(plaintext: str) -> str:
    """
    :Explain: 将明文加密为md5密文输出
    """
    if plaintext:
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode()
        return hashlib.md5(plaintext).hexdigest()
    return plaintext


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """ 
    # 生成token 
    :param subject: 保存到token的值 
    :param expires_delta: 过期时间 
    :return: 
    """
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=config.TOKEN_EXPIRE_TIME)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt
