import re
from aphone import Reader
from collections import defaultdict


RANGE10 = [str(i) for i in range(10)]


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
        rules = defaultdict(list)
        for r, v in self.rules:
            if r.txt == "":
                continue  # WTF!
            key = r.txt[0]
            r.replace = v
            rules[key].append(r.as_json())
        data['rules'] = rules
        return data

    def parse(self, txt):
        txt = txt.upper()
        prefixes = defaultdict(list)
        for r, v in self.rules:
            k = r.txt[0]
            if k != "":
                prefixes[k[0]].append((r, v))
        for v in prefixes.values():
            v.sort(sort_rules)
        result = []
        step = 0
        while txt:
            step += 1
            i = txt[0]
            if i not in prefixes:
                result.append(i)
                txt = txt[1:]
            else:
                nothing = True
                for r, v in prefixes[i]:
                    if r.match(txt, step == 1):
                        if v != "_":
                            result.append(v)
                        txt = txt[len(r.txt):]
                        nothing = False
                        continue
                if nothing:
                    result.append(i)
                    txt = txt[1:]

        return "".join(result)


def sort_rules(aa, bb):
    a = aa[0]
    b = bb[0]
    if len(a.txt) != len(b.txt):
        return len(a.txt) > len(b.txt)
    return a.priority > b.priority


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
        self.replace = ""
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
            "priority": self.priority,
            "replace": self.replace,
            "raw": self.raw
        }

    def parse(self, txt):
        if len(txt) == 0:
            self.txt = ''
            return
        if txt[-1] in RANGE10:
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
            self.txt = txt[:opening]
            self.alternates = txt[opening + 1:-1]
            return
        self.txt = txt

    def match(self, txt, first):
        if self.starting and not first:
            return False
        s = len(self.txt)
        if len(txt) < s:
            return False
        if txt[:s] != self.txt:
            return False
        if len(self.alternates) and len(txt) > s \
                and txt[s] not in self.alternates:
            return False
        if self.ending and len(txt) > s:
            return False
        return True
