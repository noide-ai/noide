from typing import Any
from jose import jwt, JWTError


def generate_jwt(payload: dict[str, Any], secret: str, algorithm: str = "RS256") -> str:
    return jwt.encode(payload, secret, algorithm=algorithm)


def jwt_is_valid(token: str) -> bool:
    try:
        payload = jwt.decode(token)
    except JWTError:
        return False

    return True