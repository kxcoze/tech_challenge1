import logging

from fastapi import Request


class CustomLogger(logging.Logger):
    """
    Custom logger for proccessing request data from FastAPI
    """

    def __init__(self, name: str, level: int = logging.NOTSET) -> None:
        super().__init__(name, level)

        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def log_with_request(self, level: int, message: str, request: Request) -> None:
        method = request.scope["method"]
        url = request.scope["path"]
        client = request.scope["client"][0]
        port = request.scope["client"][1]
        log_message = f'{message} When processing -> {client}:{port} "{method} {url}"'
        log_level_method = {
            logging.DEBUG: self.debug,
            logging.INFO: self.info,
            logging.WARNING: self.warning,
            logging.ERROR: self.error,
            logging.CRITICAL: self.critical,
        }
        log_func = log_level_method.get(level, None)
        if log_func is not None:
            log_func(log_message)
        else:
            raise ValueError(f"Unsupported log level: {level}")
