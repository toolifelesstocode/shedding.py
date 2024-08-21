import typing as t

if t.TYPE_CHECKING:
    from aiohttp import ClientSession


class Client:
    __slots__ = ("_http", "auth_token")

    if t.TYPE_CHECKING:
        _http: t.Optional[ClientSession]
        auth_token: t.Optional[str]

    def __init__(self, auth_token: t.Optional[str] = None):
        self._http = None
        self.auth_token = auth_token

    @property
    def http(self):
        if not self._http:
            self._http = ClientSession()
        return self._http

    async def request(
        self, method: str, route: str, *, auth_token: t.Optional[str] = None
    ):
        auth = auth_token or self.auth_token
        full_url = "https://developer.sepush.co.za/business/2.0" + route
        headers = {"Token": str(auth)}

        async with self.http.request(method, full_url, headers=headers) as resp:
            return await resp.json()
