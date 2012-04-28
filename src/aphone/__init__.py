

class Reader(object):
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for line in self.data:
            if len(line) == 1:
                continue
            if line[0] == '#':
                continue
            yield line[:-1]


class Header(object):
    "Aspell header, with, charset..."
    def __init__(self, txt):
        self.data = {}
        for line in Reader(txt):
            k, v = line.split(' ', 1)
            self.data[k] = v

    def __getattr__(self, key):
        if key in self.data:
            return self.data[key]
        raise AttributeError()
