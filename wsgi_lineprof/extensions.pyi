from types import CodeType
from typing import Any, Dict, Tuple


class LineTiming:
    code: Any
    lineno: int
    total_time: int
    n_hits: int

    def as_tuple(self) -> Tuple[int, int, int]: ...
    def __repr__(self) -> str: ...


class LastTime: ...


class LineProfiler:
    results: Dict[CodeType, Dict[int, LineTiming]]
    last_time: Dict[CodeType, LastTime]

    def enable(self) -> None: ...
    def disable(self) -> None: ...
    def reset(self) -> None: ...
    @staticmethod
    def get_timer() -> int: ...
    @staticmethod
    def get_timer_implementation() -> str: ...
    @staticmethod
    def get_unit() -> float: ...
