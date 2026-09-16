class StandardizedError(Exception):
    """
    error: mensaje técnico (logs)
    user_message: mensaje seguro para frontend
    http_status: código HTTP a devolver
    error_type: clasificación lógica
    error_code: código interno (SQLSTATE, etc.)
    """

    def __init__(
        self,
        error: str,
        user_message: str,
        http_status: int,
        error_type: str = "INTERNAL",
        error_code: str | None = None,
        data: dict | None = None,
    ) -> None:
        self.error = error
        self.user_message = user_message
        self.http_status = http_status
        self.error_type = error_type
        self.error_code = error_code
        self.data = data

        super().__init__(user_message)



