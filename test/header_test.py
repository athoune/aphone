import unittest
import sys
import os
from StringIO import StringIO


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../src'))

from aphone import Header


class HeaderTest(unittest.TestCase):

    def test_header(self):
        txt = """# Generated with Aspell Dicts "proc" script version 0.50.2
name fr
charset iso8859-1
special ' -*-  . -*- - -*-
soundslike fr"""
        h = Header(StringIO(txt))
        self.assertEqual('fr', h.name)
