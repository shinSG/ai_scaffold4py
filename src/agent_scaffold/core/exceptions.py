class AppError(Exception):
    def __init__(self, message: str, code: str = "APP_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ConfigurationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="CONFIGURATION_ERROR")
