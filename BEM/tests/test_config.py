"""Test the config are properly read."""

import os
from unittest import TestCase

from .. import config


class TestConfig(TestCase):
    def setUp(self):
        self.cwd_config = "default.cfg"
        self.abs_config = os.path.join(
            os.path.dirname(__file__), "default.cfg")

        self.config = {
            "binaries": [("blast", "/usr/bin/"),
                         ("blastn", "blastn"),
                         ("tblastn", "tblastn"),
                         ("makeblastdb", "makeblastdb")],
            "paths": [("output_db", "db_testing"),
                      ("input_path", ""),
                      ("output_blast", "blast_output")]}

    def test_config_directly_loads_abs_path(self):
        # An invalid file throws False
        self.assertFalse(config.read_config_values("FakeValue.cfg"))
        # A valid file returns a configparser object
        for section in self.config.keys():
            self.assertEqual(
                self.config[section],
                config.read_config_values(self.abs_config).items(section))

    def test_config_loads_cwd(self):
        # Change workind dir to ours
        from_dir = os.getcwd()
        os.chdir(os.path.dirname(__file__))

        for section in self.config.keys():
            self.assertEqual(
                self.config[section],
                config.get_config_file(self.cwd_config).items(section))

        # Reset path
        os.chdir(from_dir)

    def test_config_loads_abs_path(self):
        for section in self.config.keys():
            self.assertEqual(
                self.config[section],
                config.get_config_file(self.abs_config).items(section))

    def test_config_load_environ(self):
        # Save old environ
        old_environ = os.environ.get("BEM_CONFIG")

        os.environ["BEM_CONFIG"] = self.abs_config
        for section in self.config.keys():
            self.assertEqual(
                self.config[section],
                config.get_config_file("FakeFile.cfg").items(section))

        # Restate old environ, if any
        os.environ["BEM_CONFIG"] = old_environ or ""
