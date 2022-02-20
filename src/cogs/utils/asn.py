from dataclasses import dataclass


@dataclass(frozen=True)
class Prefixes:
    netblock: str = None
    id: str = None
    name: str = None
    country: str = None


@dataclass(frozen=True)
class ASN:
    asn: str = None
    name: str = None
    country: str = None
    allocated: str = None
    registry: str = None
    domain: str = None
    num_ips: int = None
    type: str = None
    prefixes: list = None
