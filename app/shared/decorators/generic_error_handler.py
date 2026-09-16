import inspect
import functools
from typing import Any, Callable
from app.shared.domain.models.errors import StandardizedError


def generic_error_handler(
    message: str = "Ocurrió un error inesperado.",
    silent: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        sig = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()

            self_obj = bound.arguments.get("self")
            logger = getattr(self_obj, "logger", None)

            request_id = bound.arguments.get("request_id")
            real_host = bound.arguments.get("client_host")

            try:
                return func(*args, **kwargs)

            except StandardizedError as e:
                if logger and not e.__cause__:
                    logger.error(
                        message=f"{message}: {e}",
                        request_id=request_id,
                        host=real_host,
                    )

                if silent:
                    return None
                raise

            except Exception as exc:
                if logger:
                    logger.error(
                        message=f"{message}: {exc}",
                        request_id=request_id,
                        host=real_host,
                    )
                else:
                    print(f"[ERROR-SALVADO] {message}: {exc}")

                if silent:
                    return None

                raise StandardizedError(
                    error=str(exc),
                    user_message=message,
                    http_status=500,
                    error_type="INTERNAL",
                ) from exc

        return wrapper

    return decorator