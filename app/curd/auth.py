import typing

from fastapi import Header
from sqlalchemy.orm.session import Session
from app import config
from app.core.excepts import ObjectNotFound
from app.core.depts import check_jwt_token
from app.core.security import encrypt_plaintext_md5
from app.models.auth import UserModel


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="token",
#     scopes={"me": "Read information about the current user.", "items": "Read items."},
# )


def get_user(db: Session, username: str) -> UserModel:
    """
    # 使用用户名查询用户对象
    :param db: 数据库Session实例
    :param username: 用户名
    """
    if username:
        entities = [
            UserModel.username, UserModel.hashed_password,
            UserModel.is_active, UserModel.is_admin,
            UserModel.clientid
        ]
        user = db.query(*entities).\
            filter(UserModel.username == username).first()
        return user


def get_current_user(
    db: Session, token: typing.Optional[str] = Header(None)
) -> UserModel:
    """
    根据header中token 获取当前用户
    :param db: 数据库会话
    :param token: JwtToken
    :return:
    """
    if not token:
        raise ValueError('Jwt Token为空值！')
    try:
        token_data = check_jwt_token(token)
    except:
        current_user = None
    else:
        current_user = get_user(db, token_data.get('sub'))
    if not current_user:
        raise ObjectNotFound('未找到对应的用户对象')
    return current_user


def initalize_super_user(db: Session):
    """
    在系统启动时初始化根用户
    """
    exists = get_user(db, config.SUPER_USER['username'])
    if not exists:
        super_user_info = {
            'username': config.SUPER_USER['username'],
            'password': encrypt_plaintext_md5(config.SUPER_USER['password']),
            'clientid': 0,
            'is_active': 1,
            'is_manager': 1
        }
        db.add(UserModel(**super_user_info))
        db.commit()


def add_user(db: Session, *, username: str, password: str, clientid: int = None,
        is_active: int = 1, is_manager: int = 0):
    """
    # 新增用户信息
    :param db: Session
    :param username: 用户名
    :param password: 密码
    :param clientid: ogcloud用户ID
    :param is_active: 是否激活
    :param is_manager: 是否管理员
    """
    if not all([username, password]):
        return False, '用户名或者密码不能为空！'
    exists = get_user(db, username)
    if exists:
        return False, '用户已存在！'
    userinfo = {
        'username': config.SUPER_USER['username'], 
        'password': encrypt_plaintext_md5(password),
        'is_active': is_active,
        'is_manager': is_manager
    }
    if clientid:
        userinfo.update({'clentid': clientid})
    user = UserModel(**userinfo)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> typing.Tuple[bool, str]: 
    """
    # 使用用户名&密码进行鉴权
    :param db: 数据库Session实例
    :param username: 用户名
    :param password: 密码
    :return:
        [result, errmsg]
    """
    if not all([username, password]):
        return False, '用户名或者密码不能为空！'
    user = get_user(db, username)
    if not user:
        return False, '用户不存在！'
    if user.is_active == 0:
        return False, '用户还没有启用！'
    if user.password != encrypt_plaintext_md5(password):
        return False, '用户密码错误！'
    return True, 'Success'


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
    