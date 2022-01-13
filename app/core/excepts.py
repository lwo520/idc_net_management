# Explain: 系统异常定义


class BaseError(Exception):
    def __init__(self, *args):
        if not args:
            args = ('未知错误，请联系系统管理员处理', )
        super().__init__(*args)


class TokenAuthError(BaseError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ObjectNotFound(BaseError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ObjectExistsError(BaseError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
