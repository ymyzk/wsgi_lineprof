from types import CodeType
from typing import Callable, Iterable, Union

from wsgi_lineprof.filters import BaseFilter
from wsgi_lineprof.types import CodeTiming, Measurement, RequestMeasurement


class LineProfilerStat:
    def __init__(
        self,
        code: CodeType,
        timings: CodeTiming,
    ) -> None:
        self.code = code
        self.timings = timings
        self.total_time = sum(t.total_time for t in timings.values())

    @property
    def filename(self) -> str:
        # TODO: Improve how to handle empty filename
        filename = self.code.co_filename
        return filename if filename is not None else ""

    @property
    def name(self) -> str:
        return self.code.co_name

    @property
    def firstlineno(self) -> int:
        return self.code.co_firstlineno


CallableFilterType = Callable[[Iterable[LineProfilerStat]], Iterable[LineProfilerStat]]
FilterType = Union[CallableFilterType, BaseFilter]


class LineProfilerStats:
    def __init__(self, stats: Iterable[LineProfilerStat], unit: float) -> None:
        self.stats = stats
        self.unit = unit  # seconds/hit

    @classmethod
    def from_request_measurement(
        cls, request_measurement: RequestMeasurement
    ) -> "LineProfilerStats":
        return cls.from_measurement_and_unit(
            request_measurement["results"], request_measurement["unit"]
        )

    @classmethod
    def from_measurement_and_unit(
        cls, measurement: Measurement, unit: float
    ) -> "LineProfilerStats":
        return cls([LineProfilerStat(c, t) for c, t in measurement.items()], unit)

    def filter(self, f: FilterType) -> "LineProfilerStats":
        if isinstance(f, BaseFilter):
            return LineProfilerStats(f.filter(self.stats), self.unit)
        else:
            return LineProfilerStats(f(self.stats), self.unit)
