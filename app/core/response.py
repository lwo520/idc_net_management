# Explain: 响应体定义
import functools
import typing

from fastapi import status
from fastapi.responses import JSONResponse

from typing import Union

from app.errcode import Succeed, ServerError


def ok(
        *,
        data: Union[list, dict, str] = '',
        message: str = Succeed.msg
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': Succeed.code,
            'message': message,
            'data': data,
        }
    )


def failed(
        code: int = ServerError.code,
        *,
        data: str = '',
        message: str = ServerError.msg) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': code,
            'message': message,
            'data': data,
        }
    )


def failed_errcode(err: typing.NamedTuple) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': err.code,
            'message': err.msg,
            'data': '',
        }
    )
