import uuid
from time import time
from typing import Dict, Union
from typing import Optional, Any

import jwt
from fastapi import HTTPException, status
from pydantic import SecretStr
from starlette_context import context

from app_config import settings

SecretType = Union[str, SecretStr]
JWT_ALGORITHM = "HS256"
access_lifetime = settings.ACCESS_TOKEN_EXPIRE
refresh_lifetime = settings.REFRESH_TOKEN_EXPIRE


def _get_secret(secret: SecretType) -> SecretType:
    """Get the secret key."""
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()
    return secret


def generate_jwt_token(
        identity: str,
        token_type: str,
        lifetime: int,
        secret: SecretType = settings.JWT_SECRET_KEY,
        algorithm: str = JWT_ALGORITHM,
        claims: Dict[str, Any] = None,
        headers: Dict[str, Any] = None,
) -> str:
    """
    Generate a JWT token.

    :param identity:
         The identity of this token. It can be any data that is json serializable.
    :param token_type:
        The type of the token. Can be 'access' or 'refresh'.
    :param secret:
        The secret key.
    :param lifetime:
        A value in seconds for how long this token should last before it
        expires.
    :param algorithm:
        The algorithm to use.
    :param claims:
        Optional. Additional claims to include in the token. These claims are
        merged into the default claims (exp, iat, etc)
    :param headers:
        Optional. Additional headers to include in the token. These headers
        are merged into the default headers (alg, typ)

    :return:
        The encoded JWT token.
    """
    current_time = int(time())

    payload = {
        "iat": current_time,
        "jti": str(uuid.uuid4()),
        "sub": identity,
        "type": token_type,
        "nbf": current_time,
        "exp": current_time + lifetime
    }
    payload.update(claims or {})

    return jwt.encode(
        payload,
        _get_secret(secret),
        algorithm=algorithm,
        headers=headers
    )


def decode_jwt_token(
        jwt_token: str,
        secret: SecretType = settings.JWT_SECRET_KEY,
        algorithm: str = JWT_ALGORITHM
) -> Dict[str, Any]:
    """
    Decode a JWT token.

    :param jwt_token:
        The JWT encoded token.
    :param secret:
        The secret key.
    :param algorithm:
        The algorithm to use. Defaults to 'HS256'.

    :return:
        The decoded token.
    """
    return jwt.decode(
        jwt_token,
        _get_secret(secret),
        algorithms=[algorithm]
    )


def get_jwt_identity(jwt_token: str) -> str:
    decoded_token = decode_jwt_token(jwt_token)
    return decoded_token.get("sub")


def create_access_token(
        identity: str,
        claims: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None
) -> str:
    return generate_jwt_token(
        identity=identity,
        token_type="access",
        lifetime=access_lifetime,
        claims=claims,
        headers=headers
    )


def create_refresh_token(
        identity: str,
        claims: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None
) -> str:
    return generate_jwt_token(
        identity=identity,
        token_type="refresh",
        lifetime=refresh_lifetime,
        claims=claims,
        headers=headers
    )


def get_auth_headers() -> tuple:
    """Get headers from context"""

    # forwarded_for = context.data.get('X-Forwarded-For')  # TODO: Figure out why this return None
    forwarded_for = "00.00.00.00"
    user_agent = context.data.get('User-Agent')

    if not forwarded_for:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing X-Forwarded-For header')
    elif not user_agent:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing User-Agent header')

    return forwarded_for, user_agent
