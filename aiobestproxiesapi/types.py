from typing import Optional
import enum
from dataclasses import dataclass
from datetime import datetime


class Type(enum.Enum):
    """ Тип выгружаемых прокси.
        https://best-proxies.ru/api/#params - type.

    """

    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"


class AnonymityLevel(enum.Enum):
    """ Уровень анонимности выгружаемых прокси.
        https://best-proxies.ru/api/#params - level.

    """

    HIGHLY_ANONYMOUS = 1  # высоко анонимный (элитный)
    ANONYMOUS = 2         # анонимный
    TRANSPARENT = 3       # прозрачный


@enum.unique
class Country(enum.Enum):
    """ Двубуквенные коды стран выгружаемых прокси в соответствии с ISO 3166-1 alpha-2.
        https://best-proxies.ru/api/#params - country.

    """

    AFGHANISTAN = "AF"
    ALAND_ISLANDS = "AX"
    ALBANIA = "AL"
    ALGERIA = "DZ"
    AMERICAN_SAMOA = "AS"
    ANDORRA = "AD"
    ANGOLA = "AO"
    ANGUILLA = "AI"
    ANTARCTICA = "AQ"
    ANTIGUA_AND_BARBUDA = "AG"
    ARGENTINA = "AR"
    ARMENIA = "AM"
    ARUBA = "AW"
    AUSTRALIA = "AU"
    AUSTRIA = "AT"
    AZERBAIJAN = "AZ"
    BAHAMAS = "BS"
    BAHRAIN = "BH"
    BANGLADESH = "BD"
    BARBADOS = "BB"
    BELARUS = "BY"
    BELGIUM = "BE"
    BELIZE = "BZ"
    BENIN = "BJ"
    BERMUDA = "BM"
    BHUTAN = "BT"
    BOLIVIA = "BO"
    BONAIRE_SINT_EUSTATIUS_AND_SABA = "BQ"
    BOSNIA_AND_HERZEGOVINA = "BA"
    BOTSWANA = "BW"
    BOUVET_ISLAND = "BV"
    BRAZIL = "BR"
    BRITISH_INDIAN_OCEAN_TERRITORY = "IO"
    BRUNEI_DARUSSALAM = "BN"
    BULGARIA = "BG"
    BURKINA_FASO = "BF"
    BURUNDI = "BI"
    CABO_VERDE = "CV"
    CAMBODIA = "KH"
    CAMEROON = "CM"
    CANADA = "CA"
    CAYMAN_ISLANDS = "KY"
    CENTRAL_AFRICAN_REPUBLIC = "CF"
    CHAD = "TD"
    CHILE = "CL"
    CHINA = "CN"
    CHRISTMAS_ISLAND = "CX"
    COCOS = "CC"
    COLOMBIA = "CO"
    COMOROS = "KM"
    CONGO_REPUBLIC = "CG"
    CONGO_DEMOCRATIC_REBUBLIC = "CD"
    COOK_ISLANDS = "CK"
    COSTA_RICA = "CR"
    IVORY_COAST = "CI"
    CROATIA = "HR"
    CUBA = "CU"
    CURACAO = "CW"
    CYPRUS = "CY"
    CZECHIA = "CZ"
    DENMARK = "DK"
    DJIBOUTI = "DJ"
    DOMINICA = "DM"
    DOMINICAN_REPUBLIC = "DO"
    ECUADOR = "EC"
    EGYPT = "EG"
    EL_SALVADOR = "SV"
    EQUATORIAL_GUINEA = "GQ"
    ERITREA = "ER"
    ESTONIA = "EE"
    ESWATINI = "SZ"
    ETHIOPIA = "ET"
    FALKLAND_ISLANDS = "FK"
    FAROE_ISLANDS = "FO"
    FIJI = "FJ"
    FINLAND = "FI"
    FRANCE = "FR"
    FRENCH_GUIANA = "GF"
    FRENCH_POLYNESIA = "PF"
    FRENCH_SOUTHERN_TERRITORIES = "TF"
    GABON = "GA"
    GAMBIA = "GM"
    GEORGIA = "GE"
    GERMANY = "DE"
    GHANA = "GH"
    GIBRALTAR = "GI"
    GREECE = "GR"
    GREENLAND = "GL"
    GRENADA = "GD"
    GUADELOUPE = "GP"
    GUAM = "GU"
    GUATEMALA = "GT"
    GUERNSEY = "GG"
    GUINEA = "GN"
    GUINEA_BISSAU = "GW"
    GUYANA = "GY"
    HAITI = "HT"
    HEARD_ISLAND_AND_MCDONALD_ISLANDS = "HM"
    HOLY_SEE = "VA"
    HONDURAS = "HN"
    HONG_KONG = "HK"
    HUNGARY = "HU"
    ICELAND = "IS"
    INDIA = "IN"
    INDONESIA = "ID"
    IRAN = "IR"
    IRAQ = "IQ"
    IRELAND = "IE"
    ISLE_OF_MAN = "IM"
    ISRAEL = "IL"
    ITALY = "IT"
    JAMAICA = "JM"
    JAPAN = "JP"
    JERSEY = "JE"
    JORDAN = "JO"
    KAZAKHSTAN = "KZ"
    KENYA = "KE"
    KIRIBATI = "KI"
    NORTH_KOREA = "KP"
    SOUTH_KOREA = "KR"
    KUWAIT = "KW"
    KYRGYZSTAN = "KG"
    LAOS = "LA"
    LATVIA = "LV"
    LEBANON = "LB"
    LESOTHO = "LS"
    LIBERIA = "LR"
    LIBYA = "LY"
    LIECHTENSTEIN = "LI"
    LITHUANIA = "LT"
    LUXEMBOURG = "LU"
    MACAO = "MO"
    MADAGASCAR = "MG"
    MALAWI = "MW"
    MALAYSIA = "MY"
    MALDIVES = "MV"
    MALI = "ML"
    MALTA = "MT"
    MARSHALL_ISLANDS = "MH"
    MARTINIQUE = "MQ"
    MAURITANIA = "MR"
    MAURITIUS = "MU"
    MAYOTTE = "YT"
    MEXICO = "MX"
    MICRONESIA = "FM"
    MOLDOVA = "MD"
    MONACO = "MC"
    MONGOLIA = "MN"
    MONTENEGRO = "ME"
    MONTSERRAT = "MS"
    MOROCCO = "MA"
    MOZAMBIQUE = "MZ"
    MYANMAR = "MM"
    NAMIBIA = "NA"
    NAURU = "NR"
    NEPAL = "NP"
    NETHERLANDS = "NL"
    NEW_CALEDONIA = "NC"
    NEW_ZEALAND = "NZ"
    NICARAGUA = "NI"
    NIGER = "NE"
    NIGERIA = "NG"
    NIUE = "NU"
    NORFOLK_ISLAND = "NF"
    NORTH_MACEDONIA = "MK"
    NORTHERN_MARIANA_ISLANDS = "MP"
    NORWAY = "NO"
    OMAN = "OM"
    PAKISTAN = "PK"
    PALAU = "PW"
    PALESTINE = "PS"
    PANAMA = "PA"
    PAPUA_NEW_GUINEA = "PG"
    PARAGUAY = "PY"
    PERU = "PE"
    PHILIPPINES = "PH"
    PITCAIRN = "PN"
    POLAND = "PL"
    PORTUGAL = "PT"
    PUERTO_RICO = "PR"
    QATAR = "QA"
    REUNION = "RE"
    ROMANIA = "RO"
    RUSSIA = "RU"
    RWANDA = "RW"
    SAINT_BARTHELEMY = "BL"
    SAINT_HELENA = "SH"
    SAINT_KITTS_AND_NEVIS = "KN"
    SAINT_LUCIA = "LC"
    SAINT_MARTIN = "MF"
    SAINT_PIERRE_AND_MIQUELON = "PM"
    SAINT_VINCENT_AND_THE_GRENADINES = "VC"
    SAMOA = "WS"
    SAN_MARINO = "SM"
    SAO_TOME_AND_PRINCIPE = "ST"
    SAUDI_ARABIA = "SA"
    SENEGAL = "SN"
    SERBIA = "RS"
    SEYCHELLES = "SC"
    SIERRA_LEONE = "SL"
    SINGAPORE = "SG"
    SINT_MAARTEN = "SX"
    SLOVAKIA = "SK"
    SLOVENIA = "SI"
    SOLOMON_ISLANDS = "SB"
    SOMALIA = "SO"
    SOUTH_AFRICA = "ZA"
    SOUTH_GEORGIA_AND_THE_SOUTH_SANDWICH_ISLANDS = "GS"
    SOUTH_SUDAN = "SS"
    SPAIN = "ES"
    SRI_LANKA = "LK"
    SUDAN = "SD"
    SURINAME = "SR"
    SVALBARD_AND_JAN_MAYEN = "SJ"
    SWEDEN = "SE"
    SWITZERLAND = "CH"
    SYRIAN_ARAB_REPUBLIC = "SY"
    TAIWAN = "TW"
    TAJIKISTAN = "TJ"
    TANZANIA = "TZ"
    THAILAND = "TH"
    TIMOR_LESTE = "TL"
    TOGO = "TG"
    TOKELAU = "TK"
    TONGA = "TO"
    TRINIDAD_AND_TOBAGO = "TT"
    TUNISIA = "TN"
    TURKEY = "TR"
    TURKMENISTAN = "TM"
    TURKS_AND_CAICOS_ISLANDS = "TC"
    TUVALU = "TV"
    UGANDA = "UG"
    UKRAINE = "UA"
    UNITED_ARAB_EMIRATES = "AE"
    UNITED_KINGDOM_OF_GREAT_BRITAIN_AND_NORTHERN_IRELAND = "GB"
    UNITED_STATES_OF_AMERICA = "US"
    UNITED_STATES_MINOR_OUTLYING_ISLANDS = "UM"
    URUGUAY = "UY"
    UZBEKISTAN = "UZ"
    VANUATU = "VU"
    VENEZUELA = "VE"
    VIET_NAM = "VN"
    BRITISH_VIRGIN_ISLANDS = "VG"
    UNITED_STATES_VIRGIN_ISLANDS = "VI"
    WALLIS_AND_FUTUNA = "WF"
    WESTERN_SAHARA = "EH"
    YEMEN = "YE"
    ZAMBIA = "ZM"
    ZIMBABWE = "ZW"


class Speed(enum.Enum):
    """ Скоростной грейд выгружаемых прокси.
        https://best-proxies.ru/api/#params - speed."""

    FAST = 1     # быстрые
    MIDDLE = 2   # средние по скорости
    SLOW = 3     # медленные


class ReceiveFormat(enum.Enum):
    """ Желаемый формат выгрузки прокси.
        https://best-proxies.ru/api/#common - formats.

    """

    TXT = "txt"
    CSV = "csv"
    JSON = "json"


class KeyInfoFormat(enum.Enum):
    """ Формат выгрузки данных о жизни ключа.
        https://best-proxies.ru/api/#keyinfo - format.

    """

    HOURS = "hours"
    MINUTES = "minutes"
    SECONDS = "seconds"


@dataclass()
class Proxy:
    """ Proxy-server information class. """

    ip: str
    port: int
    hostname: str
    supports_http: bool
    supports_https: bool
    supports_socks4: bool
    supports_socks5: bool
    anonymity_level: AnonymityLevel
    is_allowed_smtp: bool
    is_allowed_yandex: bool
    is_allowed_google: bool
    is_allowed_mail_ru: bool
    is_allowed_twitter: bool
    country_code: Optional[Country]
    response_ms: int
    good_count: int
    bad_count: int
    last_check_date: datetime
    city: Optional[str]
    region: Optional[str]
    real_ip: str
    test_time_secs: float

    def __str__(self):

        return self.uri

    def __hash__(self):

        return hash(self.uri)

    def __eq__(self, other):

        return self.uri == other

    @classmethod
    def from_json(cls, json: dict) -> "Proxy":
        """ Create from JSON. """

        ip = json["ip"]
        port = int(json["port"])
        hostname = json["hostname"]
        supports_http = int(json["http"])
        supports_https = int(json["https"])
        supports_socks4 = int(json["socks4"])
        supports_socks5 = int(json["socks5"])
        anonymity_level = int(json["level"])
        is_allowed_smtp = int(json["me"])
        is_allowed_yandex = int(json["yandex"])
        is_allowed_google = int(json["google"])
        is_allowed_mail_ru = int(json["mailru"])
        is_allowed_twitter = int(json["twitter"])
        country_code = json["country_code"] or None
        response_ms = int(json["response"])
        good_count = int(json["good_count"])
        bad_count = int(json["bad_count"])
        last_check_date = json["last_check"]
        city = json["city"] or None
        region = json["region"] or None
        real_ip = json["real_ip"]
        test_time_secs = float(json["test_time"])

        return cls(
            ip=ip,
            port=port,
            hostname=hostname,
            supports_http=bool(supports_http),
            supports_https=bool(supports_https),
            supports_socks4=bool(supports_socks4),
            supports_socks5=bool(supports_socks5),
            anonymity_level=AnonymityLevel(anonymity_level),
            is_allowed_smtp=bool(is_allowed_smtp),
            is_allowed_yandex=bool(is_allowed_yandex),
            is_allowed_google=bool(is_allowed_google),
            is_allowed_mail_ru=bool(is_allowed_mail_ru),
            is_allowed_twitter=bool(is_allowed_twitter),
            country_code=Country(country_code) if (country_code is not None) else None,
            response_ms=response_ms,
            good_count=good_count,
            bad_count=bad_count,
            last_check_date=datetime.strptime(last_check_date, "%Y-%m-%d %H:%M:%S"),
            city=city,
            region=region,
            real_ip=real_ip,
            test_time_secs=test_time_secs
        )

    @property
    def type(self):
        """ Type of proxy, the most reliable protocol is taken. """

        if self.supports_socks5:
            return Type.SOCKS5
        elif self.supports_socks4:
            return Type.SOCKS4
        elif self.supports_https:
            return Type.HTTPS
        elif self.supports_http:
            return Type.HTTP

    @property
    def uri(self):
        """ Proxy URI address. """

        return f"{self.type.value}://{self.ip}:{self.port}"
