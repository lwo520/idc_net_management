from collections import namedtuple


ErrBody = namedtuple('ErrBody', ['code', 'msg'])


# 通用错误码
Succeed = ErrBody(0, 'Ok')
ServerError = ErrBody(500, '系统错误')
ParamError = ErrBody(201, '参数错误')
NotFoundError = ErrBody(202, '对象不存在')


# 供应商错误码：1000~1999

# IDC错误码：2000~2999

# IP错误码：4000~4999
