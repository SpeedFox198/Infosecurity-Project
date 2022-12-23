from dataclasses import dataclass

@dataclass

class ResetPasswordBody:
    token: str
    password: str
    confirm_password: str