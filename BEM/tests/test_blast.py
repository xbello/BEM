"""Tests for the blast module."""
import os
from unittest import TestCase

from BEM import blast
from .test_mocks import Config


class testBlastN(TestCase):
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.config = Config()

        self.subject = "Small_Subject.fas"
        self.query = "Small_Query.fas"
        self.hsps = eval(open(
            os.path.join(self.path,
                         "Small_Blastn_HSP.txt")).read())

        blast.format_db(self.subject, "nucl", self.config)

        if not os.path.isdir(self.config.get("paths", "output_blast")):
            os.mkdir(self.config.get("paths", "output_blast"))

    def tearDown(self):
        db_path = self.config.get("paths", "output_db")
        for file_name in [self.subject + ".n" + ext
                          for ext in ["hr", "in", "sq"]]:
            os.unlink(os.path.join(db_path, file_name))

        os.rmdir(db_path)

        blastout_path = self.config.get("paths", "output_blast")
        for file_name in os.listdir(blastout_path):
            if file_name.endswith(".blast"):
                os.unlink(os.path.join(blastout_path, file_name))

        os.rmdir(blastout_path)

    def test_blastn(self):
        blast_hsps = blast.blastn(self.query, self.subject, self.config)

        for blast_result in blast_hsps:
            self.assertIn(blast_result, self.hsps)
