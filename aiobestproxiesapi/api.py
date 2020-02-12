

API_URL = "https://api.best-proxies.ru"


class BestProxiesAPI:

    TIMEOUT_SECS: int = 5

    def __init__(self, key: str) -> None:
        self._key = key

    @property
    def key(self):
        return self._key

    @staticmethod
    def _make_api_url():
        ...

    async def get_proxies_txt(self):
        ...

    async def get_proxies_csv(self):
        ...

    async def get_proxies_json(self):
        ...

    async def get_key_info(self):
        ...
