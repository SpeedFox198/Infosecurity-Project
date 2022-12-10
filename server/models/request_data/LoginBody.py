from dataclasses import dataclass


@dataclass
class LoginBody:
    username: str
    password: str
