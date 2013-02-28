import ConfigParser
import os

import utils

def test_config_file():
    '''config.cfg exists and is parseable'''
    config = ConfigParser.RawConfigParser()
    assert config.read('config.cfg')

    return config

def test_config_file_paths():
    #config = ConfigParser.RawConfigParser()
    required_path = ["blast"]
    required_binaries = ["blastn", "tblastn", "makeblastdb"]
    #config.read("config.cfg")
    config = test_config_file()
  
    for dir_name in required_path:
        assert os.path.isdir(config.get("binaries", dir_name)),\
            "Path doesn't exist: {0}".format(config.get("binaries", dir_name))

    for file_name in required_binaries:
        assert os.path.isfile(os.path.join(config.get("binaries", dir_name),
                config.get("binaries", file_name))),\
            "Path doesn't exist: {0}".format(config.get("binaries", file_name))

def test_format_database():
    config = test_config_file()
    mock_fasta = "test.fasta"
    expected_output = ["test.fasta.nhr", "test.fasta.nin", "test.fasta.nsq"]

    assert utils.format_database(mock_fasta),\
        "Couldn't format file {0}".format(mock_fasta)

    for file_name in expected_output:
        assert os.path.isfile(os.path.join(
                config.get("paths", "output_db"), file_name)),\
            "File doesn't exist after format database: {0}".format(
                os.path.join(config.get("paths", "output_db"),
                    file_name))
    
