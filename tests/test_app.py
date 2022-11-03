from collections import OrderedDict
from datetime import datetime
from uuid import UUID

import pytest
from pytz import utc

from wsgi_lineprof.app import ResultsApp

SHOULD_HANDLE_REQUEST_TEST_CASES = [
    ("/wsgi_lineprof/", "/wsgi_lineprof/", True),
    ("/wsgi_lineprof/", "/wsgi_lineprof/hello", True),
    ("/wsgi_lineprof/", "", False),
    ("/wsgi_lineprof/", "/hello", False),
    ("/wsgi_lineprof/", "/wsgi_lineprof", False),
]

REQUEST_1 = {
    "id": UUID("1967c955-838f-41f4-b78f-6b4adfccbaf2"),
    "started_at": datetime(2020, 1, 5, 17, 12, 53, 123, tzinfo=utc),
    "elapsed": 0.321,
    "unit": 0.001,
    "results": {},
    "request_method": "GET",
    "path_info": "/fib",
    "query_string": "",
}


class TestResultsApp:
    @pytest.fixture
    def results(self):
        return OrderedDict()

    @pytest.fixture
    def start_response(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def app(self, results):
        return ResultsApp(endpoint="/wsgi_lineprof/", results=results, filters=[])

    def test_init_enforces_trailing_slash(self, results):
        app = ResultsApp(endpoint="/wsgi_lineprof", results=results, filters=[])
        assert app.endpoint == "/wsgi_lineprof/"

    @pytest.mark.parametrize(
        "endpoint,path_info,expected", SHOULD_HANDLE_REQUEST_TEST_CASES
    )
    def test_should_handle_request(self, app, endpoint, path_info, expected):
        app.endpoint = endpoint
        env = {"PATH_INFO": path_info}
        assert app.should_handle_request(env) == expected

    def test_routing(self, mocker, app, start_response):
        env = {"PATH_INFO": "/wsgi_lineprof/"}
        handler = mocker.spy(app, "_handle_index")
        app(env, start_response)
        handler.assert_called_once_with(start_response)

    def test_index_with_empty_results(self, app, start_response, results):
        env = {"PATH_INFO": "/wsgi_lineprof/"}

        response = b"".join(app(env, start_response)).decode("utf-8")

        start_response.assert_called_once_with(
            "200 OK", [("Content-Type", "text/html; charset=utf-8")]
        )
        assert len(response) > 0
        assert "GET" not in response

    def test_index_with_results(self, app, start_response, results):
        env = {"PATH_INFO": "/wsgi_lineprof/"}
        results[REQUEST_1["id"]] = REQUEST_1

        response = b"".join(app(env, start_response)).decode("utf-8")

        start_response.assert_called_once_with(
            "200 OK", [("Content-Type", "text/html; charset=utf-8")]
        )
        assert len(response) > 0
        assert "GET" in response
        assert "/fib" in response
        assert "321" in response

    def test_detail_with_results(self, app, start_response, results):
        env = {"PATH_INFO": "/wsgi_lineprof/1967c955-838f-41f4-b78f-6b4adfccbaf2"}
        results[REQUEST_1["id"]] = REQUEST_1

        response = b"".join(app(env, start_response)).decode("utf-8")

        start_response.assert_called_once_with(
            "200 OK", [("Content-Type", "text/html; charset=utf-8")]
        )
        assert len(response) > 0
        assert "GET" in response
        assert "/fib" in response
        assert "321" in response

    def test_detail_without_results(self, app, start_response, results):
        env = {"PATH_INFO": "/wsgi_lineprof/1967c955-838f-41f4-b78f-0123456789ab"}

        response = b"".join(app(env, start_response)).decode("utf-8")

        start_response.assert_called_once_with("404 Not Found", [])
        assert len(response) == 0

    def test_detail_with_invalid_url(self, app, start_response, results):
        env = {"PATH_INFO": "/wsgi_lineprof/abcdefg"}

        response = b"".join(app(env, start_response)).decode("utf-8")

        start_response.assert_called_once_with("404 Not Found", [])
        assert len(response) == 0

    def test_not_found(self, app, start_response, results):
        env = {"PATH_INFO": "/hello"}

        response = b"".join(app(env, start_response)).decode("utf-8")

        start_response.assert_called_once_with("404 Not Found", [])
        assert len(response) == 0
