import re
from aphone import Reader


class Phonet(object):

    def __init__(self, data):
        options = ['version', 'followup', 'collapse_result', 'remove_accents']
        state = None
        spaces = re.compile(u"\s+")
        self.opt = {}
        self.rules = []
        for line in Reader(data):
            opt = False
            for option in options:
                if line.startswith("%s " % option):
                    k, v = line.split(' ', 1)
                    self.opt[k] = v
                    opt = True
                    continue
            if not opt:
                state = 'rules'
            if state == 'rules':
                rule, replacement = spaces.split(line)
                self.rules.append((Rule(rule), replacement))


class Rule(object):

    def __init__(self, txt):
        self.minus = 0
        self.ending = False
        self.again = False
        self.priority = 0
        self.parse(txt)
        print txt, self.minus, self.ending, self.again

    def __repr__(self):
        return "<Rule minus:%i ending:%s again:%s priority:%i '%s'>" % (
                self.minus, self.ending, self.again, self.priority, self.txt)

    def parse(self, txt):
        if txt[-1] in [str(i) for i in range(10)]:
            self.priority = int(txt[-1])
            self.parse(txt[:-1])
            return
        if txt[-1] == '-':
            self.minus += 1
            self.parse(txt[:-1])
            return
        if txt[-1] == '$':
            self.ending = True
            self.parse(txt[:-1])
            return
        if txt[-1] == '<':
            self.again = True
            self.parse(txt[:-1])
            return
        self.txt = txt
