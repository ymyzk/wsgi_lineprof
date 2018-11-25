from typing import Any, Dict, Tuple


class LineProfiler:
    results: Dict[Any, Any]
    last_time: Dict[Any, Any]

    def enable(self) -> None: ...
    def disable(self) -> None: ...
    @staticmethod
    def get_unit() -> float: ...


class LineTiming:
    code: Any
    lineno: int
    total_time: int
    n_hits: int

    def as_tuple(self) -> Tuple[int, int, int]: ...
    def __repr__(self) -> str: ...


class LastTime: ...
