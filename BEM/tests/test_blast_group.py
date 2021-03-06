"""Tests for the blast module."""
import os
from tempfile import _TemporaryFileWrapper
from unittest import TestCase

from BEM import blast_group


class testGrouping(TestCase):
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.GROUP_SIZE = 10

        self.query = os.path.join(self.path, "Big_Query.fas")

    def tearDown(self):
        pass

    def test_blast_group(self):
        group = blast_group.group(self.query, self.GROUP_SIZE)

        self.assertEqual(len(tuple(group)), 10)

    def test_save_bioseqs(self):
        group = blast_group.group(self.query, self.GROUP_SIZE)

        for g in group:
            temp_file = blast_group.save_bioseqs(g)
            self.assertIsInstance(temp_file, _TemporaryFileWrapper)

            temp_fasta = temp_file.readlines()

            # Assert GROUP_SIZE sequences per file
            self.assertEqual(
                len([x for x in temp_fasta if x.startswith(">")]),
                self.GROUP_SIZE)

    def test_group_to_files(self):
        group_files = blast_group.files(self.query, self.GROUP_SIZE)

        files_tuple = tuple(group_files)

        self.assertEqual(len(files_tuple), 10)

        self.assertIsInstance(files_tuple[0], _TemporaryFileWrapper)
        self.assertEqual(len(files_tuple[0].readlines()), 30)
