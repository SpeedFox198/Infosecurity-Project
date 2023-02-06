import re

from pydantic import BaseModel, validator


class ScanURLBody(BaseModel):
    urls: list[str]
    message_id: str

    @validator("urls")
    def check_url(cls, value):
        url_regex = r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'

        for url in value:
            if not re.fullmatch(url_regex, url):
                print("Invalid URL")
                raise ValueError("Invalid URL.")

        return value
