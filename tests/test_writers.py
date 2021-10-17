import threading

from wsgi_lineprof.stats import LineProfilerStats
from wsgi_lineprof.writers import AsyncStreamWriter, SyncStreamWriter


class TestSyncStreamWriter:
    def test_write_calls_format_stats(self, mocker):
        stream = mocker.Mock()
        formatter = mocker.Mock()
        writer = SyncStreamWriter(stream, formatter)
        stats = LineProfilerStats([], 0.001)

        writer.write(stats)

        formatter.format_stats.assert_called_once_with(stats, stream)


class TestAsyncStreamWriter:
    def test_write_calls_format_stats(self, mocker):
        stream = mocker.Mock()
        formatter = mocker.Mock()
        writer = AsyncStreamWriter(stream, formatter)
        stats = LineProfilerStats([], 0.001)

        writer.write(stats)
        writer._join()

        formatter.format_stats.assert_called_once_with(stats, stream)

    def test_write_when_none_is_given(self, mocker):
        stream = mocker.Mock()
        formatter = mocker.Mock()
        writer = AsyncStreamWriter(stream, formatter)

        writer.write(None)
        writer._join()

        formatter.format_stats.assert_not_called()

    def test_join_stops_thread(self, mocker):
        original_active_thread_count = threading.active_count()
        writer = AsyncStreamWriter(mocker.Mock(), mocker.Mock())
        assert original_active_thread_count + 1 == threading.active_count()

        writer._join()

        assert original_active_thread_count == threading.active_count()
