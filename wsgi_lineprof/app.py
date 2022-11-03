import re
from io import StringIO
from typing import TYPE_CHECKING, Any, Dict, Iterable
from uuid import UUID

from jinja2 import Environment, PackageLoader

from wsgi_lineprof.formatter import TextFormatter
from wsgi_lineprof.stats import FilterType, LineProfilerStats
from wsgi_lineprof.types import RequestMeasurement
from wsgi_lineprof.writers import SyncStreamWriter

if TYPE_CHECKING:
    from wsgiref.types import StartResponse, WSGIEnvironment


UUID_RE = re.compile(
    "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", re.I
)


class ResultsApp:
    """WSGI application to show the profiling results"""

    def __init__(
        self,
        endpoint: str,
        results: Dict[UUID, RequestMeasurement],
        filters: Iterable[FilterType],
    ) -> None:
        assert endpoint.startswith("/")
        if not endpoint.endswith("/"):
            endpoint += "/"
        self.endpoint = endpoint
        self.results = results
        self.filters = filters
        self.template_env = Environment(
            loader=PackageLoader("wsgi_lineprof", "templates"), autoescape=True
        )

    def __call__(
        self, env: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        if not self.should_handle_request(env):
            return _return_404(start_response)

        path = env["PATH_INFO"][len(self.endpoint) :]
        if path == "":
            return self._handle_index(start_response)
        elif UUID_RE.match(path):
            return self._handle_detail(start_response, UUID(path))
        else:
            return _return_404(start_response)

    def should_handle_request(self, env: "WSGIEnvironment") -> bool:
        """Returns true only if this app should handle the request"""
        return bool(env["PATH_INFO"].startswith(self.endpoint))

    def _handle_index(self, start_response: "StartResponse") -> Iterable[bytes]:
        template = self.template_env.get_template("index.html")
        # To suppress the following mypy error on Python 3:
        # error: No overload variant of "reversed" matches argument
        results: Any = self.results.values()
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [template.render(results=reversed(results)).encode("utf-8")]

    def _handle_detail(
        self, start_response: "StartResponse", request_id: UUID
    ) -> Iterable[bytes]:
        request_measurement = self.results.get(request_id)
        if request_measurement is None:
            return _return_404(start_response)

        template = self.template_env.get_template("detail.html")
        stream: Any = StringIO()
        writer = SyncStreamWriter(stream, TextFormatter(color=False))
        stats = LineProfilerStats.from_request_measurement(request_measurement)
        for f in self.filters:
            stats = stats.filter(f)
        writer.write(stats)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [
            template.render(result=request_measurement, stats=stream.getvalue()).encode(
                "utf-8"
            )
        ]


def _return_404(start_response: "StartResponse") -> Iterable[bytes]:
    start_response("404 Not Found", [])
    return []
