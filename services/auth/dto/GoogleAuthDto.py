from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GoogleAuthDto:
    authorization_code: str = field(default=None)
    access_token: str = field(default=None)
    refresh_token: str = field(default=None)
    expiration: datetime or None = field(default=None)

    def to_dict(self):
        return {
            'authorization_code': self.authorization_code,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expiration': self.expiration.strftime("%Y/%m/%d %H:%M:%S") if self.expiration else None
        }