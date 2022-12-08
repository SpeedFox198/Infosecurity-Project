from dataclasses import dataclass
from typing import List


@dataclass
class DeviceData:
    id: str
    time: int
    location: str
    os: str
    browser: str


@dataclass
class DeviceListData:
    devices: List[DeviceData]
