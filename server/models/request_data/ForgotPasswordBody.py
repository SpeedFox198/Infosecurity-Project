from dataclasses import dataclass


@dataclass
class ForgotPasswordBody:
    email: str
