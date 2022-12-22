from dataclasses import dataclass

@dataclass

class ResetPasswordBody:
    password: str
    confirm_password: str