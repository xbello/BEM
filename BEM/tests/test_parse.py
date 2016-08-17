"""Tests for parser."""
import json
import os
from unittest import TestCase

from BEM import parse


class testParseBlastn(TestCase):
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.blast_output = open(os.path.join(
            self.path, "Small_Blastn_Output.txt")).read()

        with open(os.path.join(self.path, "Small_Blastn_HSP.json")) as j:
            self.HSP_output = json.load(j)

    def test_blast_tab(self):
        parsed_dict = parse.blast_tab(self.blast_output)

        self.assertEqual([x for x in parsed_dict],
                         self.HSP_output)
