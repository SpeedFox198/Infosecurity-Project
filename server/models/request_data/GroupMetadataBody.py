from pydantic import BaseModel, validator
from quart.datastructures import FileStorage


class GroupMetadataBody(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    icon: FileStorage | None
    name: str
    disappearing: str
    users: list[str]

    @validator("icon")
    def check_icon(cls, value):
        if value is None:
            return value

        if value.mimetype not in ("image/jpeg", "image/png", "image/gif"):
            raise ValueError("Invalid file type.")

        return value

    @validator("name")
    def check_group_name(cls, value):
        if not value:
            raise ValueError("Group name should not be empty.")

        return value

    @validator("disappearing")
    def check_disappearing(cls, value):
        if value not in ("off", "24h", "7d", "30d"):
            raise ValueError("Invalid disappearing messages option.")

        return value

    @validator("users")
    def check_users(cls, value):
        if not value:
            raise ValueError("Group should have 1 included participant.")
        
        return value
