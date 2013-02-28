import ConfigParser
import os

def test_config_file():
    '''config.cfg exists and is parseable'''
    config = ConfigParser.RawConfigParser()
    assert config.read('config.cfg')

def test_config_file_paths():
    config = ConfigParser.RawConfigParser()
    required_path = ["blast"]
    required_binaries = ["blastn", "tblastn"]
    config.read("config.cfg")
  
    for dir_name in required_path:
        assert os.path.isdir(config.get("binaries", dir_name)),\
            "Path doesn't exist: {0}".format(config.get("binaries", dir_name))

    for file_name in required_binaries:
        assert os.path.isfile(config.get("binaries", file_name))
    
