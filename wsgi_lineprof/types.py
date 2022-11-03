import uuid
from datetime import datetime
from types import CodeType
from typing import Dict, TextIO

from typing_extensions import TypedDict

from wsgi_lineprof.extensions import LineTiming

CodeTiming = Dict[int, LineTiming]
Measurement = Dict[CodeType, CodeTiming]
RequestMeasurement = TypedDict(
    "RequestMeasurement",
    {
        "id": uuid.UUID,
        "started_at": datetime,
        "elapsed": float,
        "unit": float,
        "results": Measurement,
        "request_method": str,
        "path_info": str,
        "query_string": str,
    },
)

# TODO: Improve definition
Stream = TextIO
