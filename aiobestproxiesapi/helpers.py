from typing import Optional
import urllib.parse


def make_url(url: str, route: str, params: Optional[dict] = None,
             join_params: bool = False, encoding: str = "UTF-8") -> str:
    """ Build URL from components. """

    url = f"{url}/{route}"

    if params is not None:
        if join_params:
            for key, value in params.items():
                if isinstance(value, (list, tuple)):
                    params[key] = ",".join(map(str, value))
        params_encoded: str = urllib.parse.urlencode(params, encoding=encoding)

        url = f"{url}?{params_encoded}"

    return url
