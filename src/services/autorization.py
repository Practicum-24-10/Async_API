import jwt
from fastapi import Header, Depends, HTTPException
from jwt import ExpiredSignatureError, InvalidSignatureError, DecodeError

from src.auth.abc_key import AbstractKey
from src.auth.rsa_key import get_pk
from src.local.services import autorization as errors


async def get_token_payload(
        authorization: str | None = Header(None),
        pk: AbstractKey = Depends(get_pk)
) -> None | dict[str, list[str]]:
    if authorization is not None:
        scheme, token = authorization.split(" ")
        try:
            payload = jwt.decode(token, pk.key, algorithms=pk.algorithms)
            return {'is_superuser': payload[pk.pl_is_superuser],
                    'permissions': payload[pk.pl_permissions]}
        except ExpiredSignatureError:
            raise HTTPException(status_code=403,
                                detail=errors.TOKEN_EXPIRED)
        except InvalidSignatureError:
            raise HTTPException(status_code=403,
                                detail=errors.TOKEN_VER_FAILED)
        except DecodeError:
            raise HTTPException(status_code=403,
                                detail=errors.TOKEN_BAD_DECODE)
        except KeyError:
            raise HTTPException(status_code=403,
                                detail=errors.TOKEN_BAD_PAYLOAD)
    return None
