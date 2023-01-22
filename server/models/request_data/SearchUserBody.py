from pydantic import BaseModel, validator


class SearchUserBody(BaseModel):
    username: str

    @validator("username")
    def check_username(cls, value):
        if not value:
            raise ValueError("Username should not be empty.")

        return value
