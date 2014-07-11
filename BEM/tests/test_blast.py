"""Tests for the blast module."""
import os
from unittest import TestCase

from Bio import SeqIO

from BEM import blast
from .test_mocks import Config


class testFormatDatabase(TestCase):
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.config = Config()
        self.fasta = os.path.join("subject.fas")
        self.db_path = self.config.get("paths", "output_db")
        self.expected = ["subject.fas.nhr",
                         "subject.fas.nin",
                         "subject.fas.nsq"]

    def tearDown(self):
        for file_name in self.expected:
            if os.path.isfile(os.path.join(self.db_path, file_name)):
                os.unlink(os.path.join(self.db_path, file_name))
        if os.path.isdir(self.db_path):
            os.rmdir(self.db_path)

    def test_formatn_database(self):
        stdout = blast.format_db(self.fasta, "nucl", self.config)
        self.assertTrue(stdout.split("\n")[2].startswith(
            "Building a new DB, current time:"))

    def test_checkn_output(self):
        blast.format_db(self.fasta, "nucl", self.config)

        expected_output = ["subject.fas.nhr",
                           "subject.fas.nin",
                           "subject.fas.nsq"]
        for file_name in expected_output:
            self.assertTrue(
                os.path.isfile(os.path.join(self.db_path, file_name)))


class testBlastN(TestCase):
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.config = Config()

        self.subject = os.path.join("subject.fas")
        self.query = os.path.join("dna_query.fas")

        blast.format_db(self.subject, "nucl", self.config)

        if not os.path.isdir(self.config.get("paths", "output_blast")):
            os.mkdir(self.config.get("paths", "output_blast"))

    def tearDown(self):
        db_path = self.config.get("paths", "output_db")
        for file_name in [
                "subject.fas.nhr", "subject.fas.nin", "subject.fas.nsq"]:
            os.unlink(os.path.join(db_path, file_name))

        os.rmdir(db_path)

        blastout_path = self.config.get("paths", "output_blast")
        for file_name in os.listdir(blastout_path):
            if file_name.endswith(".blast"):
                os.unlink(os.path.join(blastout_path, file_name))

        os.rmdir(blastout_path)

    def test_blastn(self):
        stdout = blast.blastn(self.query, self.subject, self.config)
        self.assertEqual(
            stdout.split("\n")[0],
            "Mock_DNA_sequence\tDrosophila\t99.48\t382" +\
            "\t0\t1\t1\t382\t67\t446\t2e-128\t 445")

    def test_split_query(self):
        subject = "tests/Small_Subject.fas"

        for pack in blast.split_query(subject, n=10):
            seqs_pack = list(SeqIO.parse(pack.name, "fasta"))
            # Check all the files have 10 or less sequences
            self.assertTrue(len(seqs_pack) <= 10)
            os.unlink(pack.name)
