from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from jose import jwt, JWTError

from app.core.config import settings
from auth.security.token_constants import (
    ACCESS_TOKEN_LEEWAY_SECONDS,
    ACCESS_TOKEN_TTL_MINUTES,
    ALGORITHM
)

@dataclass(slots=True, frozen=True)
class TokenService:
    """
    Stateless - Сервис для работы с JWT-токенами.

    - HS256 по умолчанию.
    - Чёткое соблюдение временных меток.
    - Дополнительные поля issuer/audience (опционально).
    - Не зависит от FastAPI или ORM.
    """
    secret: str
    algorithm: str = ALGORITHM
    access_ttl: timedelta = timedelta(minutes=ACCESS_TOKEN_TTL_MINUTES)
    issuer: str | None = None
    audience: str | None = None
    leeway_seconds: int = ACCESS_TOKEN_LEEWAY_SECONDS

    def provide_access_token(
        self,
        sub: str,
        **extra: Any
    ) -> str:
        now = self._now()
        expires = now + self.access_ttl
        payload: Dict[str, Any] = {
            'sub': sub,
            'iat': int(now.timestamp()),
            'nbf': int(now.timestamp()),
            'exp': int(expires.timestamp()),
            'type': 'access',
        }
        if self.issuer:
            payload['iss'] = self.issuer
        if self.audience:
            payload['aud'] = self.audience
        if extra:
            payload.update(extra)
        headers = {
            'typ': 'JWT',
            'alg': self.algorithm
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=self.algorithm,
            headers=headers
        )

    def decode_access(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                issuer=self.issuer if self.issuer else None,
                audience=self.audience if self.audience else None,
                options={
                'require_exp': True,
                    'require_iat': True,
                    'require_nbf': True,
                },
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверный токен доступа',
            )
        if payload.get('type') != 'access':
            raise JWTError('Неверный тип токена')
        return payload

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)