from wsgi_lineprof.stats import LineProfilerStats
from wsgi_lineprof.writers import SyncStreamWriter


class TestSyncStreamWriter(object):
    def test_write_calls_format_stats(self, mocker):
        stream = mocker.Mock()
        formatter = mocker.Mock()
        writer = SyncStreamWriter(stream, formatter)
        stats = LineProfilerStats([], 0.001)

        writer.write(stats)

        formatter.format_stats.assert_called_once_with(stats, stream)
