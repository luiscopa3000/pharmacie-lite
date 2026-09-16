from typing import Optional, Protocol, runtime_checkable
from app.auth.domain.models.user_password import UserPassword


@runtime_checkable
class IAuthByPasswordRepository(Protocol):
    def execute(
        self,
        user: Optional[str] = None,
        email: Optional[str] = None,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> UserPassword:
        ...

    def get_user_for_login(
        self,
        user: Optional[str] = None,
        email: Optional[str] = None,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> Optional[UserPassword]:
        ...

@runtime_checkable
class IRegisterUserRepository(Protocol):
    def execute(
        self,
        role_id: int,
        username: str,
        email: str,
        password_hash: str,
        full_name: str,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ) -> int:
        ...