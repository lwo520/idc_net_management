import hashlib
import uuid


class TokenAuthError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.errmsg = str(args[0])


class UserNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.errmsg = str(args[0])


def get_hashcode(plain_text: str) -> str:
    if plain_text:
        return hashlib.md5(plain_text.encode()).hexdigest()
    return ''


def gen_uuid() -> str:
    # 生成uuid
    return uuid.uuid4().hex
