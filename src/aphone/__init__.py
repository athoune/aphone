

class Header(object):
    "Aspell header, with, charset..."
    def __init__(self, txt):
        self.data = {}
        for line in txt.split("\n"):
            if len(line) and line[0] == '#':
                continue
            k, v = line.split(' ', 1)
            self.data[k] = v

    def __getattr__(self, key):
        if key in self.data:
            return self.data[key]
        raise AttributeError()
