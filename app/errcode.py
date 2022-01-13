from collections import namedtuple


ErrBody = namedtuple('ErrBody', ['code', 'msg'])


class ErrCode:
    SUCCESS = ErrBody(0, 'Success')
    SEVER_ERROR = ErrBody(500, 'Server Error.')
    # 供应商错误码：1001~1999
    VENDOR_EXISTS = ErrBody(1001, '供应商已存在')
