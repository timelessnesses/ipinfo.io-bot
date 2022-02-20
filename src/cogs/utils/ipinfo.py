from dataclasses import dataclass


@dataclass(frozen=True)
class Domains:
    total: int = 0
    domains: list = None


@dataclass(frozen=True)
class Abuse:
    address: str = None
    country: str = None
    email: str = None
    name: str = None
    network: str = None
    phone: str = None


@dataclass(frozen=True)
class Privacy:
    vpn: bool = None
    proxy: bool = None
    tor: bool = None
    relay: bool = None
    hosting: bool = None
    service: str = None


@dataclass(frozen=True)
class Company:
    name: str = None
    domain: str = None
    type: str = None


@dataclass(frozen=True)
class ASN:
    asn: str = None
    name: str = None
    domain: str = None
    route: str = None
    type: str = None


@dataclass(
    frozen=True,
    order=False,
)
class IP:
    ip: str = None
    hostname: str = None
    city: str = None
    region: str = None
    country: str = None
    loc: str = None
    org: str = None
    postal: str = None
    timezone: str = None
    asn: ASN = None
    company: Company = None
    abuse: Abuse = None
    domains: Domains = None
    privacy: Privacy = None
