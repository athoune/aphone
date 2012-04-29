# -*- encoding: utf-8 -*-
import unittest
import sys
import os
from StringIO import StringIO


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../src'))

from aphone.phonet import Phonet

sample = """
#   Copyright (C) 2000 Rémi Vanicat
version francais 0.000000001

#EMME ~ AME
AIX$               E
AI                 E
AN(AEUIO)-         AM
AN                 A
AMM                AM
AM(AEUIO)-         AM
AM                 A
AUD$               O
AUX$		   O
AU                 O
A                  A

TOTO<              O

"""


class PhonetTest(unittest.TestCase):

    def testRead(self):
        p = Phonet(StringIO(sample))
        print p.as_json()
