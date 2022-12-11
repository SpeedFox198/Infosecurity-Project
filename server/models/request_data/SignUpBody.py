from dataclasses import dataclass

@dataclass
class SignUpBody:
    username: str
    password: str
    email: str