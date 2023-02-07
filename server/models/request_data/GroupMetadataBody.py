import magic
from pydantic import BaseModel, validator


class GroupMetadataBody(BaseModel):
    icon: bytes | None
    icon_name: str | None
    name: str
    disappearing: str
    users: list[str]

    @validator("icon")
    def check_icon(cls, value):
        if value is None:
            return value

        file_magic = magic.Magic(mime=True)
        icon_mimetype = file_magic.from_buffer(value)
        if icon_mimetype not in ("image/jpeg", "image/png"):
            raise ValueError("Invalid file type.")

        return value

    @validator("name")
    def check_group_name(cls, value):
        if not value:
            raise ValueError("Group name should not be empty.")

        return value

    @validator("disappearing")
    def check_disappearing(cls, value):
        # TODO(low)(SpeedFox198): remove demo values
        if value not in ("off", "5s", "15s", "24h", "7d", "30d"):
            raise ValueError("Invalid disappearing messages option.")

        return value

    @validator("users")
    def check_users(cls, value):
        if not value:
            raise ValueError("Group should have 1 included participant.")

        return value
