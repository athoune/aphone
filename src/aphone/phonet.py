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
                rule, replacement = spaces.split(line)[:2]
                self.rules.append((Rule(rule), replacement))

    def as_json(self):
        data = self.opt
        rules = {}
        for r, v  in self.rules:
            if r.txt == "":
                continue  # WTF!
            key = r.txt[0]
            if key not in rules:
                rules[key] = []
            rules[key].append((r.as_json(), v))
        data['rules'] = rules
        return data


class Rule(object):

    def __init__(self, txt):
        self.raw = txt
        self.minus = 0  # -
        self.ending = False  # $
        self.starting = False  # ^
        self.again = False  # <
        self.separately = False  # ^^
        self.alternates = ""
        self.priority = 5
        self.parse(txt)

    def __unicode__(self):
        return u"<Rule minus:%i ending:%s again:%s priority:%i '%u'>" % (
                self.minus, self.ending, self.again, self.priority, self.txt)

    def as_json(self):
        return {
            "text": self.txt,
            "alternates": self.alternates,
            "minus": self.minus,
            "ending": self.ending,
            "starting": self.starting,
            "again": self.again,
            "priority": self.priority
                }

    def parse(self, txt):
        if len(txt) == 0:
            self.txt = ''
            return
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
        if txt[-1] == '^':
            if self.starting:  # ^^
                self.starting = False
                self.separately = True
            else:
                self.starting = True
            self.parse(txt[:-1])
            return
        if txt[-1] == '<':
            self.again = True
            self.parse(txt[:-1])
            return
        if txt[-1] == ')':
            opening = txt.find('(')
            print txt, txt[:opening], txt[opening + 1:-1]
            self.txt = txt[:opening]
            self.alternates = txt[opening + 1:-1]
            return
        self.txt = txt
