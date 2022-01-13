import hashlib
import uuid
from functools import wraps

from pydantic import ValidationError

from .excepts import ObjectNotFound, ObjectExistsError
from .response import ok, failed
from .log import logger
from .depts import get_db


def get_hashcode(plain_text: str) -> str:
    if plain_text:
        return hashlib.md5(plain_text.strip().encode()).hexdigest()
    return ''


def gen_uuid() -> str:
    # 生成uuid
    return uuid.uuid4().hex


def curd_deco(curd_f):
    @wraps(curd_f)
    def _wrap(*args, **kwargs):
        db = args[0]
        try:
            return curd_f(*args, **kwargs)
        except (ObjectNotFound, ObjectExistsError) as e:
            raise e
        except Exception as e:
            logger.error(e.args[0])
        db.rollback()
        return False, None
    return _wrap

