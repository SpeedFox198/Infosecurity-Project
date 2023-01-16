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
        self._dark_mode = None
        self._malware_scan = None
        self._friends_only = None
        self._censor = None
        self._twofa_status = None

    async def _resolve(self):
        if not self._resolved:
            try:
                self._user_id, self._device_id = self.auth_id.split(".")
            except (ValueError, AttributeError):
                self._user_id, self._device_id = ("",)*2

            user_details = await get_user_details(self._user_id) or ("",) * 8

            (
                self._username,
                self._email,
                self._avatar,
                self._dark_mode,
                self._malware_scan,
                self._friends_only,
                self._censor,
                self._twofa_status
            ) = user_details

            self._resolved = True

    @property
    async def user_id(self):
        await self._resolve()
        return self._user_id

    @property
    async def device_id(self):
        await self._resolve()
        return self._device_id

    @property
    async def username(self):
        await self._resolve()
        return self._username

    @property
    async def email(self):
        await self._resolve()
        return self._email

    @property
    async def avatar(self):
        await self._resolve()
        return self._avatar

    @property
    async def dark_mode(self):
        await self._resolve()
        return self._dark_mode

    @property
    async def malware_scan(self):
        await self._resolve()
        return self._malware_scan

    @property
    async def friends_only(self):
        await self._resolve()
        return self._friends_only

    @property
    async def censor(self):
        await self._resolve()
        return self._censor

    @property
    async def twofa_status(self):
        await self._resolve()
        return self._twofa_status
