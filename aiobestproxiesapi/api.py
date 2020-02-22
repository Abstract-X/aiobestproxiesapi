import asyncio
from asyncio import AbstractEventLoop
from typing import Optional, Union, List, Tuple, Any, NoReturn
import json as jsonlib

from aiohttp import ClientSession, ClientResponse

from . import helpers, exceptions
from .params import Param
from .types import Type, AnonymityLevel, Country, Speed, ReceiveFormat, KeyInfoFormat, Proxy


API_URL = "https://api.best-proxies.ru"

TIMEOUT_SECS: int = 5
MAX_AMOUNT_PROXIES = 15000


class BestProxiesAPI:
    """ Wrapper for https://best-proxies.ru/api/. """

    def __init__(self, key: str, loop: Optional[AbstractEventLoop] = None) -> None:
        """ Initialization.

        :param key:     Authorization key for best-proxies API.
        :param loop:    Asyncio event loop.
        """

        self._key = Param.KEY.prepare_func(key)
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop

    async def __aenter__(self) -> "BestProxiesAPI":
        """ Creating a aiohttp.ClientSession for 'async with' block. """

        self.__session = ClientSession(loop=self._loop)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """ Closing a aiohttp.ClientSession for 'async with' block. """

        await self.__session.close()

    @property
    def key(self) -> str:
        """ Authorization key, protected from overriding. """

        return self._key

    @staticmethod
    def __parse_reason_503_error(content: bytes) -> str:
        """ Parsing the cause of the error from the server response. """

        html: str = content.decode(encoding="UTF-8")
        body_block = html.rsplit("<body>")[-1]
        reason = body_block.rsplit("<p>Ошибка авторизации: ")[-1].split("</p>")[0]

        return reason

    @staticmethod
    def __raise_specific_503_error(reason: str) -> NoReturn:
        """ Throwing an exception with an incorrect 503 server response. """

        for comments, exception in (
                (("Указанный ключ не активирован",), exceptions.KeyIsNotActivatedError),
                (("Период действия этого ключа окончен",), exceptions.KeyExpiredError),
                (("Ключ указан неверно",), exceptions.IncorrectKeyError),
                (("Вы исчерпали количество попыток неправильного ввода ключей",
                  "Вы исчерпали предел попыток неправильного ввода ключа подряд"), exceptions.TooManyKeyAttemptsError)
        ):
            for comment in comments:
                if reason.startswith(comment):
                    raise exception(reason)

        raise exceptions.InternalServerError(reason)

    @staticmethod
    def _make_api_url(route: str, params: Optional[dict] = None) -> str:
        """ Make an API url. """

        return helpers.make_url(url=API_URL, route=route, params=params, join_params=True)

    async def __process_response_error(self, status_code: int, content: bytes):
        """ Processing response error and raising a specific exception. """

        if status_code == 503:
            reason = await self._loop.run_in_executor(None, self.__parse_reason_503_error, content)
            self.__raise_specific_503_error(reason=reason)

    async def __process_response(self, response: ClientResponse) -> bytes:
        """ Receiving content and throwing exceptions when an incorrect response. """

        status_code = response.status
        content = await response.read()

        if status_code == 200:
            return content
        else:
            await self.__process_response_error(status_code=status_code, content=content)

        raise exceptions.APIError(f"status_code: '{status_code}',\n"
                                  f"content: '{content}'")

    def _prepare_params(self, params: List[Tuple[Param, Any]]) -> dict:
        """ Preparing parameters for sending request to API. """

        prepared_params = {
            Param.KEY.param_name: self._key
        }

        for param, value in params:
            value = param.prepare_func(value)
            if value is not None:
                prepared_params[param.param_name] = value

        return prepared_params

    async def _send_api_request(self, route: str, method: str,
                                params: List[Tuple[Param, Any]]) -> bytes:
        """ Sending API request. """

        prepared_params = self._prepare_params(params=params)
        url = self._make_api_url(route=route, params=prepared_params)

        async with self.__session.request(method=method, url=url) as response:
            content = await self.__process_response(response=response)

        return content

    async def _get_proxies_content_with_api_params(
            self,
            *,
            receive_format: ReceiveFormat,
            type_: Union[List[Union[Type, str]], Type, str, None] = None,
            level: Union[List[Union[AnonymityLevel, int]], AnonymityLevel, int, None] = None,
            ports: Union[List[int], int, None] = None,
            pex: Optional[int] = None,
            country: Union[List[Union[Country, str]], Country, str, None] = None,
            cex: Optional[bool] = None,
            response: Optional[int] = None,
            uptime: Optional[int] = None,
            speed: Union[List[Union[Speed, int]], Speed, int, None] = None,
            mail: Optional[bool] = None,
            yandex: Optional[bool] = None,
            google: Optional[bool] = None,
            mailru: Optional[bool] = None,
            twitter: Optional[bool] = None,
            includeType: Optional[bool] = None,
            limit: int = 0,
            nocascade: Optional[bool] = None,
            filename: Optional[str] = None
    ) -> bytes:
        """ Getting proxy method content for further processing. """

        content = await self._send_api_request(
            route=f"proxylist.{receive_format.value}",
            method="GET",
            params=[
                (Param.TYPE, type_),
                (Param.LEVEL, level),
                (Param.PORTS, ports),
                (Param.PEX, pex),
                (Param.COUNTRY, country),
                (Param.CEX, cex),
                (Param.RESPONSE, response),
                (Param.UPTIME, uptime),
                (Param.SPEED, speed),
                (Param.MAIL, mail),
                (Param.YANDEX, yandex),
                (Param.GOOGLE, google),
                (Param.MAILRU, mailru),
                (Param.TWITTER, twitter),
                (Param.INCLUDE_TYPE, includeType),
                (Param.LIMIT, limit),
                (Param.NOCASCADE, nocascade),
                (Param.FILENAME, filename)
            ]
        )

        # service may return empty data
        if content == b"":
            raise exceptions.NoProxiesError()

        return content

    async def get_proxies(
            self,
            *,
            types: Union[List[Union[Type, str]], Type, str, None] = None,
            anonimity_levels: Union[List[Union[AnonymityLevel, int]], AnonymityLevel, int, None] = None,
            ports: Union[List[int], int, None] = None,
            exclude_ports: Optional[bool] = None,
            countries: Union[List[Union[Country, str]], Country, str, None] = None,
            exclude_countries: Optional[bool] = None,
            response_ms: Optional[int] = None,
            uptime_hours: Optional[int] = None,
            speeds: Union[List[Union[Speed, int]], Speed, int, None] = None,
            is_allowed_smtp: Optional[bool] = None,
            is_allowed_yandex: Optional[bool] = None,
            is_allowed_google: Optional[bool] = None,
            is_allowed_mail_ru: Optional[bool] = None,
            is_allowed_twitter: Optional[bool] = None,
            include_type: Optional[bool] = None,
            limit: int = 0,
            exclude_cascade: Optional[bool] = None
    ) -> List[Proxy]:
        """ Getting list proxies (objects) from JSON content. """

        proxies = await self.get_proxies_json(types=types, anonimity_levels=anonimity_levels,
                                              ports=ports, exclude_ports=exclude_ports,
                                              countries=countries, exclude_countries=exclude_countries,
                                              response_ms=response_ms, uptime_hours=uptime_hours,
                                              speeds=speeds, is_allowed_smtp=is_allowed_smtp,
                                              is_allowed_yandex=is_allowed_yandex,
                                              is_allowed_google=is_allowed_google,
                                              is_allowed_mail_ru=is_allowed_mail_ru,
                                              is_allowed_twitter=is_allowed_twitter,
                                              include_type=include_type, limit=limit,
                                              exclude_cascade=exclude_cascade)
        proxies = [Proxy.from_json(i) for i in proxies]
        return proxies

    @staticmethod
    def __save_proxies_in_file(proxies_content: str, filename: str) -> None:
        """ Saving proxies content in file. """

        with open(file=f"{filename}.txt", mode="w", encoding="UTF-8") as file_:
            file_.write(proxies_content)

    async def get_proxies_txt_with_api_params(
            self,
            *,
            type_: Union[List[Union[Type, str]], Type, str, None] = None,
            level: Union[List[Union[AnonymityLevel, int]], AnonymityLevel, int, None] = None,
            ports: Union[List[int], int, None] = None,
            pex: Optional[int] = None,
            country: Union[List[Union[Country, str]], Country, str, None] = None,
            cex: Optional[bool] = None,
            response: Optional[int] = None,
            uptime: Optional[int] = None,
            speed: Union[List[Union[Speed, int]], Speed, int, None] = None,
            mail: Optional[bool] = None,
            yandex: Optional[bool] = None,
            google: Optional[bool] = None,
            mailru: Optional[bool] = None,
            twitter: Optional[bool] = None,
            includeType: Optional[bool] = None,
            limit: int = 0,
            nocascade: Optional[bool] = None,
            filename: Optional[str] = None
    ) -> List[str]:
        """ Getting list proxies (URIs) using original API parameters. """

        content = await self._get_proxies_content_with_api_params(receive_format=ReceiveFormat.TXT, type_=type_,
                                                                  level=level, ports=ports, pex=pex, country=country,
                                                                  cex=cex, response=response, uptime=uptime,
                                                                  speed=speed, mail=mail, yandex=yandex, google=google,
                                                                  mailru=mailru, twitter=twitter,
                                                                  includeType=includeType, limit=limit,
                                                                  nocascade=nocascade, filename=filename)
        content = content.decode(encoding="UTF-8")

        if filename:
            await self._loop.run_in_executor(None, self.__save_proxies_in_file, content, filename)

        proxies = content.splitlines()
        return proxies

    async def get_proxies_txt(
            self,
            *,
            types: Union[List[Union[Type, str]], Type, str, None] = None,
            anonimity_levels: Union[List[Union[AnonymityLevel, int]], AnonymityLevel, int, None] = None,
            ports: Union[List[int], int, None] = None,
            exclude_ports: Optional[bool] = None,
            countries: Union[List[Union[Country, str]], Country, str, None] = None,
            exclude_countries: Optional[bool] = None,
            response_ms: Optional[int] = None,
            uptime_hours: Optional[int] = None,
            speeds: Union[List[Union[Speed, int]], Speed, int, None] = None,
            is_allowed_smtp: Optional[bool] = None,
            is_allowed_yandex: Optional[bool] = None,
            is_allowed_google: Optional[bool] = None,
            is_allowed_mail_ru: Optional[bool] = None,
            is_allowed_twitter: Optional[bool] = None,
            include_type: Optional[bool] = None,
            limit: int = 0,
            exclude_cascade: Optional[bool] = None,
            filename: Optional[str] = None
    ) -> List[str]:
        """ Getting list proxies (URIs) using normalized API parameters (aliases). """

        return await self.get_proxies_txt_with_api_params(type_=types, level=anonimity_levels, ports=ports,
                                                          pex=exclude_ports, country=countries,
                                                          cex=exclude_countries, response=response_ms,
                                                          uptime=uptime_hours, speed=speeds,
                                                          mail=is_allowed_smtp, yandex=is_allowed_yandex,
                                                          google=is_allowed_google, mailru=is_allowed_mail_ru,
                                                          twitter=is_allowed_twitter, includeType=include_type,
                                                          limit=limit, nocascade=exclude_cascade, filename=filename)

    async def get_proxies_csv_with_api_params(
            self,
            *,
            type_: Union[List[Union[Type, str]], Type, str, None] = None,
            level: Union[List[Union[AnonymityLevel, int]], AnonymityLevel, int, None] = None,
            ports: Union[List[int], int, None] = None,
            pex: Optional[int] = None,
            country: Union[List[Union[Country, str]], Country, str, None] = None,
            cex: Optional[bool] = None,
            response: Optional[int] = None,
            uptime: Optional[int] = None,
            speed: Union[List[Union[Speed, int]], Speed, int, None] = None,
            mail: Optional[bool] = None,
            yandex: Optional[bool] = None,
            google: Optional[bool] = None,
            mailru: Optional[bool] = None,
            twitter: Optional[bool] = None,
            includeType: Optional[bool] = None,
            limit: int = 0,
            nocascade: Optional[bool] = None
    ) -> str:
        """ Getting proxies (CSV-content) using original API parameters. """

        content = await self._get_proxies_content_with_api_params(receive_format=ReceiveFormat.CSV,
                                                                  type_=type_, level=level, ports=ports, pex=pex,
                                                                  country=country, cex=cex, response=response,
                                                                  uptime=uptime, speed=speed, mail=mail, yandex=yandex,
                                                                  google=google, mailru=mailru, twitter=twitter,
                                                                  includeType=includeType, limit=limit,
                                                                  nocascade=nocascade)
        proxies: str = content.decode(encoding="windows-1251")
        return proxies

    async def get_proxies_csv(
            self,
            *,
            types: Union[List[Union[Type, str]], Type, str, None] = None,
            anonimity_levels: Union[List[Union[AnonymityLevel, int]], AnonymityLevel, int, None] = None,
            ports: Union[List[int], int, None] = None,
            exclude_ports: Optional[bool] = None,
            countries: Union[List[Union[Country, str]], Country, str, None] = None,
            exclude_countries: Optional[bool] = None,
            response_ms: Optional[int] = None,
            uptime_hours: Optional[int] = None,
            speeds: Union[List[Union[Speed, int]], Speed, int, None] = None,
            is_allowed_smtp: Optional[bool] = None,
            is_allowed_yandex: Optional[bool] = None,
            is_allowed_google: Optional[bool] = None,
            is_allowed_mail_ru: Optional[bool] = None,
            is_allowed_twitter: Optional[bool] = None,
            include_type: Optional[bool] = None,
            limit: int = 0,
            exclude_cascade: Optional[bool] = None
    ) -> str:
        """ Getting proxies (CSV-content) using normalized API parameters (aliases). """

        return await self.get_proxies_csv_with_api_params(type_=types, level=anonimity_levels, ports=ports,
                                                          pex=exclude_ports, country=countries, cex=exclude_countries,
                                                          response=response_ms, uptime=uptime_hours, speed=speeds,
                                                          mail=is_allowed_smtp, yandex=is_allowed_yandex,
                                                          google=is_allowed_google, mailru=is_allowed_mail_ru,
                                                          twitter=is_allowed_twitter, includeType=include_type,
                                                          limit=limit, nocascade=exclude_cascade)

    async def get_proxies_json_with_api_params(
            self,
            *,
            type_: Union[List[Union[Type, str]], Type, str, None] = None,
            level: Union[List[Union[AnonymityLevel, int]], AnonymityLevel, int, None] = None,
            ports: Union[List[int], int, None] = None,
            pex: Optional[int] = None,
            country: Union[List[Union[Country, str]], Country, str, None] = None,
            cex: Optional[bool] = None,
            response: Optional[int] = None,
            uptime: Optional[int] = None,
            speed: Union[List[Union[Speed, int]], Speed, int, None] = None,
            mail: Optional[bool] = None,
            yandex: Optional[bool] = None,
            google: Optional[bool] = None,
            mailru: Optional[bool] = None,
            twitter: Optional[bool] = None,
            includeType: Optional[bool] = None,
            limit: int = 0,
            nocascade: Optional[bool] = None
    ) -> List[dict]:
        """ Getting list proxies (JSON) using original API parameters. """

        content = await self._get_proxies_content_with_api_params(receive_format=ReceiveFormat.JSON,
                                                                  type_=type_, level=level, ports=ports, pex=pex,
                                                                  country=country, cex=cex, response=response,
                                                                  uptime=uptime, speed=speed, mail=mail, yandex=yandex,
                                                                  google=google, mailru=mailru, twitter=twitter,
                                                                  includeType=includeType, limit=limit,
                                                                  nocascade=nocascade)
        proxies: List[dict] = jsonlib.loads(content.decode(encoding="UTF-8"))
        return proxies

    async def get_proxies_json(
            self,
            *,
            types: Union[List[Union[Type, str]], Type, str, None] = None,
            anonimity_levels: Union[List[Union[AnonymityLevel, int]], AnonymityLevel, int, None] = None,
            ports: Union[List[int], int, None] = None,
            exclude_ports: Optional[bool] = None,
            countries: Union[List[Union[Country, str]], Country, str, None] = None,
            exclude_countries: Optional[bool] = None,
            response_ms: Optional[int] = None,
            uptime_hours: Optional[int] = None,
            speeds: Union[List[Union[Speed, int]], Speed, int, None] = None,
            is_allowed_smtp: Optional[bool] = None,
            is_allowed_yandex: Optional[bool] = None,
            is_allowed_google: Optional[bool] = None,
            is_allowed_mail_ru: Optional[bool] = None,
            is_allowed_twitter: Optional[bool] = None,
            include_type: Optional[bool] = None,
            limit: int = 0,
            exclude_cascade: Optional[bool] = None
    ) -> List[dict]:
        """ Getting list proxies (JSON) using normalized API parameters. """

        return await self.get_proxies_json_with_api_params(type_=types, level=anonimity_levels, ports=ports,
                                                           pex=exclude_ports, country=countries, cex=exclude_countries,
                                                           response=response_ms, uptime=uptime_hours, speed=speeds,
                                                           mail=is_allowed_smtp, yandex=is_allowed_yandex,
                                                           google=is_allowed_google, mailru=is_allowed_mail_ru,
                                                           twitter=is_allowed_twitter, includeType=include_type,
                                                           limit=limit, nocascade=exclude_cascade)

    async def get_key_info(self, format_: Union[KeyInfoFormat, str] = KeyInfoFormat.HOURS) -> int:
        """ Getting key lifetime information. """

        content = await self._send_api_request(
            route="key.txt",
            method="GET",
            params=[
                (Param.FORMAT, format_)
            ]
        )
        key_info = int(content.decode())
        return key_info
