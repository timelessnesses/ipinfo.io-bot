from dataclasses import dataclass


@dataclass(frozen=True)
class IPRanges:
    domain: str = None
    num_ranges: int = None
    ranges: list = None
