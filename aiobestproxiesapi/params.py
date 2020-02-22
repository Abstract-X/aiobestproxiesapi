from typing import Optional, Any, List
import enum
from enum import EnumMeta
import string as stringlib
import functools

from . import exceptions
from .types import Type, AnonymityLevel, Country, Speed, KeyInfoFormat


def _prepare_param(param: Any, enum_type: Optional[EnumMeta] = None) -> Any:
    """ General parameter preparation. """

    if isinstance(param, bool):
        if param is True:
            return 1
        else:
            return None

    if param is not None:
        if enum_type is not None:
            if not isinstance(param, enum_type):
                param = enum_type(param)
            return param.value

    return param


def _prepare_param_list(param: Any, sort_list: bool = False, max_amount: Optional[int] = None,
                        enum_type: Optional[EnumMeta] = None) -> List[Any]:
    """ Preparing a parameter with a list value. """

    if param is not None:
        if not isinstance(param, list):
            param = [param]
        else:
            if max_amount:
                if len(param) > max_amount:
                    raise exceptions.TooManyValuesParamError(f"Max: {max_amount}, expected: {param}.")
        if enum_type is not None:
            if not isinstance(param, enum_type):
                param = [enum_type(i) for i in param]

        param = [i.value for i in param]

        if sort_list:
            param.sort()

        return param


def _prepare_param_key(key):
    """ Key parameter preparation. """

    incorrect_exception = ValueError(f"Invalid key: '{key}'.")

    if len(key) != 32:
        raise incorrect_exception

    for c in key:
        if c not in (stringlib.ascii_lowercase + stringlib.digits):
            raise incorrect_exception

    return key


def _prepare_param_uptime(uptime):
    """ Uptime parameter preparation. """

    if uptime is not None:
        if 0 < uptime < 1:
            return f"{int(uptime * 60)}m"

        if not (1 <= uptime <= 48):
            raise ValueError(f"Invalid uptime: '{uptime}'.")

        return uptime


def _prepare_param_filename(filename):
    """ Filename parametr preparation. """

    if filename is not None:

        invalid_error = ValueError(f"Invalid filename: '{filename}'.")

        if not (3 <= len(filename) <= 10):
            raise invalid_error

        for c in filename:
            if c not in (stringlib.ascii_letters + stringlib.digits):
                raise invalid_error

    return filename


class Param(enum.Enum):
    """ API parameters.
        https://best-proxies.ru/api/#params
    """

    KEY = ("key", _prepare_param_key)
    TYPE = ("type", functools.partial(_prepare_param_list,
                                      sort_list=True, enum_type=Type))
    LEVEL = ("level", functools.partial(_prepare_param_list,
                                        sort_list=True, enum_type=AnonymityLevel))
    PORTS = ("ports", functools.partial(_prepare_param_list,
                                        max_amount=5))
    PEX = ("pex", _prepare_param)
    COUNTRY = ("country", functools.partial(_prepare_param_list,
                                            sort_list=True, max_amount=20, enum_type=Country))
    CEX = ("cex", _prepare_param)
    RESPONSE = ("response", _prepare_param)
    UPTIME = ("uptime", _prepare_param_uptime)
    SPEED = ("speed", functools.partial(_prepare_param_list,
                                        sort_list=True, enum_type=Speed))
    MAIL = ("mail", _prepare_param)
    YANDEX = ("yandex", _prepare_param)
    GOOGLE = ("google", _prepare_param)
    MAILRU = ("mailru", _prepare_param)
    TWITTER = ("twitter", _prepare_param)
    INCLUDE_TYPE = ("includeType", _prepare_param)
    LIMIT = ("limit", _prepare_param)
    NOCASCADE = ("nocascade", _prepare_param)
    FILENAME = ("filename", _prepare_param_filename)
    FORMAT = ("format", functools.partial(_prepare_param, enum_type=KeyInfoFormat))

    @property
    def param_name(self):
        """ Original API parameter name. """

        return self.value[0]

    @property
    def prepare_func(self):
        """ Function of preparing the value to normalize it. """

        return self.value[1]
