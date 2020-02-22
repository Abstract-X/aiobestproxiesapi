# AIOBestProxiesAPI
Asynchronous API wrapper for [best-proxies.ru](https://best-proxies.ru/api/) using aiohttp.

## Installation
Install/update with [pip](https://pip.pypa.io/en/stable/):
``` shell
pip install aiobestproxiesapi -U
```
**I recommend using a [virtual environment](https://docs.python.org/3.7/library/venv.html).**

## Usage
The simplest example:
``` python
import asyncio
from aiobestproxiesapi import BestProxiesAPI


KEY = "..."  # insert your key here


async def main():
    async with BestProxiesAPI(key=KEY) as api:
        proxies = await api.get_proxies()

    # proxies received and ready to go...


if __name__ == '__main__':
    asyncio.run(main())
```
This will return a list of `Proxy` objects that you can already work with:
``` python
# properties
proxy.uri                 # socks5://177.XXX.75.117:53054
proxy.type                # Type.SOCKS5

# attrs
proxy.ip                  # '177.XXX.75.117'
proxy.port                # 53054
proxy.hostname            # 'example.host.za'
proxy.supports_http       # False
proxy.supports_https      # False
proxy.supports_socks4     # False
proxy.supports_socks5     # True
proxy.anonymity_level     # AnonymityLevel.ANONYMOUS
proxy.is_allowed_smtp     # True
proxy.is_allowed_yandex   # True
proxy.is_allowed_google   # False
proxy.is_allowed_mail_ru  # True
proxy.is_allowed_twitter  # False
proxy.country_code        # Country.BRAZIL
proxy.response_ms         # 257
proxy.good_count          # 20
proxy.bad_count           # 0
proxy.last_check_date     # datetime.datetime(2020, 2, 22, 17, 0, 49)
proxy.city                # 'Example-City'
proxy.region              # 'Example-Region'
proxy.real_ip             # '177.XXX.75.117'
proxy.test_time_secs      # 2.3
```
**Proxy [obj]** is also easy to cast to string type:
``` python
str(proxy)  # "socks5://177.XXX.75.117:53054"
proxy.uri   # "socks5://177.XXX.75.117:53054"
```

**You can also specify filters.**  
Description of the parameters can be found [here](https://best-proxies.ru/api/#params).
``` python
from aiobestproxiesapi.types import Type, AnonymityLevel, Country, Speed

async def main():
    async with BestProxiesAPI(key=KEY) as api:
        proxies = await api.get_proxies(
            types=[Type.HTTPS, Type.SOCKS5],
            anonimity_levels=AnonymityLevel.ANONYMOUS,
            ports=[80, 443, 1080, 3128, 8080],
            countries=[Country.BRAZIL, Country.RUSSIA],
            response_ms=500,
            uptime_hours=2,
            speeds=[Speed.MIDDLE, Speed.FAST],
            is_allowed_smtp=True,
            include_type=True
        )
```

If you need proxies in raw format, you can receive them by choosing the appropriate method:
``` python
proxies_txt = await api.get_proxies_txt(...)
proxies_csv = await api.get_proxies_csv(...)
proxies_json = await api.get_proxies_json(...)
```

**Attention!** In the examples shown, the names of the original parameters were replaced with more appropriate aliases. You can use the original parameters, if necessary:
``` python
await api.get_proxies_txt_with_api_params(
    type_=...,
    level=...,
    ports=...,
    pex=...,
    country=...,
    cex=...,
    response=...,
    uptime=...,
    speed=...,
    mail=...,
    yandex=...,
    google=...,
    mailru=...,
    twitter=...,
    includeType=...,
    limit=...,
    nocascade=...,
    filename=...
)
await api.get_proxies_csv_with_api_params(
    ...
)
await api.get_proxies_json_with_api_params(
    ...
)
```

Get information about the life of the authorization key:
``` python
import asyncio
from aiobestproxiesapi import BestProxiesAPI
from aiobestproxiesapi.types import KeyInfoFormat


KEY = "..."  # insert your key here


async def main():
    async with BestProxiesAPI(key=KEY) as api:
        secs_left: int = await api.get_key_info(format_=KeyInfoFormat.SECONDS)  # hours/minutes/seconds


if __name__ == '__main__':
    asyncio.run(main())
```

You can use raw values for parameters, instead of `aiobestproxies.types`. Enum-types are offered for convenience only.
``` python
# from aiobestproxiesapi.types import Type, AnonymityLevel, Country, Speed

async def main():
    async with BestProxiesAPI(key=KEY) as api:
        proxies = await api.get_proxies(
            types=["https", "socks5"],
            anonimity_levels=2,
            ports=[80, 443, 1080, 3128, 8080],
            countries=["BR", "RU"],
            response_ms=500,
            uptime_hours=2,
            speeds=[1, 2],
            is_allowed_smtp=1,
            include_type=1
        )
```
