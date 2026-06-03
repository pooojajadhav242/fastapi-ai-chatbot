from passlib.hash import pbkdf2_sha256
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

def hash_password(password: str):
    return pbkdf2_sha256.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pbkdf2_sha256.verify(
        plain_password,
        hashed_password
    )



def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None    