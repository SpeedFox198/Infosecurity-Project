from dataclasses import dataclass

@dataclass
class LoginCallBackBody:
    token: str
    access_token: str
    scope: str
    token_type: str
    expires_in: int