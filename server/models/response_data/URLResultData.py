from dataclasses import dataclass


@dataclass
class URLResultData:
    harmless: int
    malicious: int
    suspicious: int
    undetected: int
    timeout: int
