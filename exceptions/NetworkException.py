from dataclasses import dataclass, field

@dataclass
class NetworkException(Exception):

    def __init__(self, message: str = '', status_code: int = 400, payload: dict = {}) -> None:
        self.message = message
        self.status_code = status_code
        self.payload = payload