from six import StringIO


class StringNoopIO(StringIO):
    def write(self, *args, **kwargs):
        pass
