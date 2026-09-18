from typing import Protocol, runtime_checkable

from app.identity.domain.models.token import AccessTokenClaims, IssuedAccessToken


@runtime_checkable
class IAccessTokenService(Protocol):
    def issue(self, subject: int) -> IssuedAccessToken: ...

    def verify(self, token: str) -> AccessTokenClaims: ...
