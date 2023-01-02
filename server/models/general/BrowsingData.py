from dataclasses import dataclass


@dataclass
class BrowsingData:
    browser: str
    os: str
    location: str
