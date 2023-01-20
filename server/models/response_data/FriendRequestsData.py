from dataclasses import dataclass

from models.response_data import FriendData


@dataclass
class FriendRequestsData:
    sent: list[FriendData]
    received: list[FriendData]
