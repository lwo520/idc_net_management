# Explain: 响应体定义
import typing

from typing import Union
from pydantic import BaseModel

from app.errcode import Succeed, ServerError


def ok(*,
       data: Union[list, dict, str, BaseModel] = '',
       message: str = Succeed.msg) -> typing.Dict:
    return {
        'code': Succeed.code,
        'data': data,
        'message': message,
    }


def failed(
        code: int = ServerError.code,
        *,
        data: str = '',
        message: str = ServerError.msg
) -> typing.Dict:
    return {
        'code': code,
        'message': message,
        'data': data,
    }


def failed_errcode(err: typing.NamedTuple) -> typing.Dict:
    return {
            'code': err.code,
            'message': err.msg,
            'data': '',
        }
