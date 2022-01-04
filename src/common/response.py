# Explain: 响应体定义

from fastapi import status
from fastapi.responses import JSONResponse

from typing import Union


def ok(*, data: Union[list, dict, str]=None, message: str="Success"):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'message': message,
            'data': data,
        }
    )


def failed(*,  code: int = 500, data: str = None, message: str="系统错误"):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': code,
            'message': message,
            'data': data,
        }
    )
