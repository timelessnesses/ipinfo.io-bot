from dataclasses import dataclass


@dataclass(frozen=True)
class HostedDomain:
    ip: str = None
    total: int = 0
    domains: list = None
