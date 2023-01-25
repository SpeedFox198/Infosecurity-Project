from dataclasses import dataclass


@dataclass
class UserData:
    user_id: str
    device_id: str
    username: str
    email: str
    avatar: str | None
    public_key: str | None
    dark_mode: bool
    malware_scan: bool
    friends_only: bool
    censor: bool
    twofa_status: bool
