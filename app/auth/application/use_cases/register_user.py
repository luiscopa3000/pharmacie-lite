from typing import Optional

from app.shared.decorators import generic_error_handler
from app.shared.domain.interfaces.logger import ILogger
from app.shared.domain.interfaces.security import IPasswordHasher

from app.auth.domain.interfaces.repositories import IRegisterUserRepository
from app.auth.application.dto.register_request import RegisterRequest


class RegisterUser:
    """
    Caso de uso para registrar a un nuevo usuario.
    Toma la contraseña en texto plano, la hashea usando IPasswordHasher,
    y persiste al usuario en la base de datos usando el repositorio.
    """

    def __init__(
        self,
        logger: ILogger,
        register_user_repo: IRegisterUserRepository,
        password_hasher: IPasswordHasher,
    ) -> None:
        self.logger = logger
        self.register_user_repo = register_user_repo
        self.password_hasher = password_hasher

    @generic_error_handler()
    def execute(
        self,
        register_request: RegisterRequest,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ) -> int:
        
        self.logger.info(
            f"Intentando registrar al usuario: {register_request.username}",
            request_id=request_id,
            host=host,
        )

        # Hashear la contraseña con salt+pepper
        hashed_password = self.password_hasher.hash(register_request.password)

        # Guardar en base de datos
        user_id = self.register_user_repo.execute(
            role_id=register_request.role_id,
            username=register_request.username,
            email=register_request.email,
            password_hash=hashed_password,
            full_name=register_request.full_name,
            request_id=request_id,
            host=host,
            current_user_id=current_user_id,
        )

        self.logger.info(
            f"Usuario registrado exitosamente con ID: {user_id}",
            request_id=request_id,
            host=host,
        )

        return user_id
