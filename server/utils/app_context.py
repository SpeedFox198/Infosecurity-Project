from quart_auth import Quart


class AppContext:
    """
    App Context Manager

    Usage: access Quart app from other parts of the poject

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

    @property
    def secret_key(self) -> str:
        """ Quart app's secret key """
        return self.app.secret_key
