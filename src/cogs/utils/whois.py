from dataclasses import dataclass

@dataclass(frozen=True)
class NetInfoRecords:
    range: str = None
    id: str = None
    country: str = None
    name: str = None
    organization: str = None
    admin: str = None
    abuse: str = None
    tech: str = None
    maintainer: str = None
    updated: str = None
    status: str = None
    source: str = None
    raw: str = None
    created: str = None

@dataclass(frozen=True)
class NetInfo:
    net: str = None
    total: int = None
    records: list = None

@dataclass(frozen=True)
class POCInfoRecords:
    id: str = None
    name: str = None
    email: str = None
    phone: str = None
    address: str = None
    country: str = None
    phone: str = None
    fax: str = None
    created: str = None
    updated: str = None
    source: str = None
    raw: str = None

@dataclass(frozen=True)
class POCInfo:
    poc: str = None
    total: int = None
    records: list = None