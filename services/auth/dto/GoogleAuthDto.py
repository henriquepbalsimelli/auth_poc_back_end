from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GoogleAuthDto:
    authorization_code: str = field(default=None)
    access_token: str = field(default=None)
    refresh_token: str = field(default=None)
    expiration: datetime or None = field(default=None)
