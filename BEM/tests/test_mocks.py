"""Mock objects for testing."""
import os


class Config(object):
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.values = {
            "binaries": {
                "blast": "/usr/bin/",
                "blastn": "blastn",
                "tblastn": "tblastn",
                "makeblastdb": "makeblastdb"},
            "paths": {
                "output_db": os.path.join(self.path, "db_testing"),
                "input_path": self.path,
                "output_blast": os.path.join(self.path, "blast_output")},
            "blastn": {
                "task": "blastn",
                "evalue": "1",
                "word": "11",
                "penalty": "-5",
                "reward": "5",
                "gapopen": "10",
                "gapextend": "10"}
        }

    def get(self, entry, key):
        return self.values[entry][key]

    def set(self, entry, key, value):
        self.values.setdefault(entry, {})
        self.values[entry][key] = value
