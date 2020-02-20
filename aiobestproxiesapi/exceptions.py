

class TooManyValuesParamError(Exception):
    """ Too many parameter values passed while sending request. """


class APIError(Exception):
    """ Unknown error, incorrect API response. """


class NoProxiesError(Exception):
    """ There are no proxies, the server returned empty data. """


class UnknownStatusCodeError(Exception):
    """ Server responded with an unknown status code. """


# INTERNAL SERVER ERRORS

class InternalServerError(Exception):
    """ Internal server error: 503 status code. """


class KeyExpiredError(InternalServerError):
    """ Authorization key has expired. """


class KeyIsNotActivatedError(InternalServerError):
    """ Authorization key was not activated, before accessing the service. """


class IncorrectKeyError(InternalServerError):
    """ Authorization key is incorrect. """


class TooManyKeyAttemptsError(InternalServerError):
    """ Too many requests were sent, the server temporarily blocked access. """
