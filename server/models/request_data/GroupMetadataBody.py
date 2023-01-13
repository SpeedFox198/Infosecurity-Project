from pydantic import BaseModel, validator


class GroupMetaDataBody(BaseModel):
    name: str
    disappearing: str
    users: list[str]

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
