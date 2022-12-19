from quart_auth import BadSignature, Quart, _AuthSerializer, _get_config_or_default
from werkzeug.sansio.http import parse_cookie
from models import AuthedUser


class SioAuthManager:
    """
    SocketIO Authentication Manager

    Register a Quart app with `init_app` function.

    Raises RuntimeError if property is read without registering app.
    """

    def __init__(self) -> None:
        self._app = None


    def register_app(self, app: Quart) -> None:
        """ Registers a Quart app """
        self._app = app


    @property
    def app(self) -> Quart:
        """ Current Quart app """
        if self._app is None:
            raise RuntimeError("App is not registered")
        return self._app


    def get_user(self, cookie) -> AuthedUser:
        """ Returns the current user after authenticating the user """
        auth_id = self.load_cookie(cookie)

        return AuthedUser(auth_id)


    def load_cookie(self, cookie: str) -> str | None:
        try:
            # TODO(SpeedFox198): Consider catching possible error when parsing error
            cookie = parse_cookie(cookie) 
            token = cookie[_get_config_or_default("QUART_AUTH_COOKIE_NAME", self.app)]
        except KeyError:
            return None
        else:
            serializer = _AuthSerializer(
                self.app.secret_key,
                _get_config_or_default("QUART_AUTH_SALT", self.app),
            )
            try:
                return serializer.loads(token)
            except BadSignature:
                return None