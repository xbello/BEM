import ConfigParser
import os

from BEM import blast
from BEM import utils

def test_config_file():
    '''config.cfg exists and is parseable'''
    config = ConfigParser.RawConfigParser()
    assert config.read('config.cfg')

    return config

def test_config_file_paths():
    required_path = ["blast"]
    required_binaries = ["blastn", "tblastn", "makeblastdb"]
    config = test_config_file()

    for dir_name in required_path:
        assert os.path.isdir(config.get("binaries", dir_name)),\
            "Path doesn't exist: {0}".format(config.get("binaries", dir_name))

    for file_name in required_binaries:
        assert os.path.isfile(os.path.join(config.get("binaries", dir_name),
                config.get("binaries", file_name))),\
            "Path doesn't exist: {0}".format(config.get("binaries", file_name))

class testFormatDatabase():
    def setUp(self):
        self.path = os.path.split(__file__)[0]
        self.config = ConfigParser.RawConfigParser()
        self.config.read(os.path.join(self.path, 'config.cfg'))
        self.config.set('paths', 'output_db', os.path.join(self.path,
            self.config.get('paths', 'output_db')))
        self.config.set('paths', 'input_path', os.path.join(self.path,
            self.config.get('paths', 'input_path')))
        self.fasta = "subject.fas"
        self.db_path = self.config.get("paths", "output_db")
        self.expected = ["subject.fas.nhr", "subject.fas.nin",
            "subject.fas.nsq"]

    def tearDown(self):
        for file_name in self.expected:
            os.unlink(os.path.join(self.db_path, file_name))
        os.rmdir(self.db_path)

    def test_formatn_database(self):
        assert utils.format_database(self.fasta, "nucl", self.config),\
            "Couldn't format file {0}".format(self.fasta)

    def test_checkn_output(self):
        utils.format_database(self.fasta, "nucl", self.config)

        expected_output = ["subject.fas.nhr", "subject.fas.nin",
            "subject.fas.nsq"]
        for file_name in expected_output:
            assert os.path.isfile(os.path.join(self.db_path, file_name)),\
                "File doesn't exist after format database: {0}".format(
                os.path.join(self.db_path, file_name))

class testBlastN():
    def setUp(self):
        self.path = os.path.split(__file__)[0]
        self.config = ConfigParser.RawConfigParser()
        self.config.read('config.cfg')
        self.config.read(os.path.join(self.path, 'config.cfg'))
        self.config.set('paths', 'output_db', os.path.join(self.path,
            self.config.get('paths', 'output_db')))
        self.config.set('paths', 'input_path', os.path.join(self.path,
            self.config.get('paths', 'input_path')))
        self.config.set('paths', 'output_blast', os.path.join(self.path,
            self.config.get('paths', 'output_blast')))

        self.subject = "subject.fas"
        self.query = os.path.join(self.path, "dna_query.fas")

        utils.format_database(self.subject, "nucl", self.config)

        if not os.path.isdir("blast_output"): os.mkdir("blast_output")

    def tearDown(self):
        db_path = os.path.join(self.config.get("paths", "output_db"))
        for file_name in ["subject.fas.nhr", "subject.fas.nin",
            "subject.fas.nsq"]:
            os.unlink(os.path.join(db_path, file_name))

        os.rmdir(db_path)

    def test_blastn(self):
        assert utils.blastn(self.query, self.subject, self.config),\
            "Couldn't blast {0} against {1}".format(self.query, self.subject)

    def test_blastn_output(self):
        #TODO DEBUG This isn't testing anything but formatdb output
        utils.blastn(self.query, self.subject, self.config)

        expected = ["subject.fas.nhr", "subject.fas.nin", "subject.fas.nsq"]

        for x in expected:
            assert os.path.isfile(os.path.join(
                self.config.get("paths", "output_db"), x)),\
                "File doesn't exist after blasting: {0}".format(
                    os.path.join(self.path, "blast_output", x))

    def test_validate_output(self):
       utils.blastn(self.query, self.subject, self.config)

       with open(os.path.join(self.config.get("paths", "output_blast"),
           self.subject + ".blast"), "r") as output:
           assert output.readlines()[0].split() == \
               ["Mock_DNA_sequence", "Drosophila", "99.48", "382", "0", "1",
                "1", "382", "67", "446", "2e-128", "445"]
