from quart_auth import AuthUser

from db_access.user import get_user_details


class AuthedUser(AuthUser):
    def __init__(self, auth_id):
        super().__init__(auth_id)
        self._resolved = False
        self._user_id = None
        self._device_id = None
        self._username = None
        self._email = None
        self._avatar = None
        self._public_key = None
        self._dark_mode = None
        self._malware_scan = None
        self._friends_only = None
        self._censor = None
        self._google_account = None
        self._disappearing = None

    async def _resolve(self):
        if not self._resolved:
            try:
                self._user_id, self._device_id = self.auth_id.split(".")
            except (ValueError, AttributeError):
                self._user_id, self._device_id = ("",)*2

            user_details = await get_user_details(self._user_id) or ("",) * 10

            (
                self._username,
                self._email,
                self._avatar,
                self._public_key,
                self._dark_mode,
                self._malware_scan,
                self._friends_only,
                self._censor,
                self._google_account,
                self._disappearing
            ) = user_details

            self._resolved = True

    @property
    async def user_id(self) -> str:
        await self._resolve()
        return self._user_id

    @property
    async def device_id(self) -> str:
        await self._resolve()
        return self._device_id

    @property
    async def username(self) -> str:
        await self._resolve()
        return self._username

    @property
    async def email(self) -> str:
        await self._resolve()
        return self._email

    @property
    async def avatar(self) -> str:
        await self._resolve()
        return self._avatar

    @property
    async def public_key(self) -> str:
        await self._resolve()
        return self._public_key

    @property
    async def dark_mode(self) -> bool:
        await self._resolve()
        return self._dark_mode

    @property
    async def malware_scan(self) -> bool:
        await self._resolve()
        return self._malware_scan

    @property
    async def friends_only(self) -> bool:
        await self._resolve()
        return self._friends_only

    @property
    async def censor(self) -> bool:
        await self._resolve()
        return self._censor

    @property
    async def google_account(self) -> bool:
        await self._resolve()
        return self._google_account

    @property
    async def disappearing(self) -> bool:
        await self._resolve()
        return self._disappearing
