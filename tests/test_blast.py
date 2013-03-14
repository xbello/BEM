import ConfigParser
import os

from nose import with_setup

import blast
import utils

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

def teardown_format():
    config = test_config_file()
    for x in ["subject.fas.nhr", "subject.fas.nin", "subject.fas.nsq",
              "subject.fas.phr", "subject.fas.pin", "subject.fas.psq"]:
        if os.path.isfile(os.path.join(
            config.get("paths", "output_db"), "tests", x)):
            os.unlink(os.path.join(
                config.get("paths", "output_db"), "tests", x))

@with_setup(teardown_format)
def test_format_database():
    config = test_config_file()
    mock_fasta = "tests/subject.fas"
    expected_output = ["subject.fas.nhr", "subject.fas.nin", "subject.fas.nsq"]

    for db_type in ["nucl", "prot"]:
        assert utils.format_database(mock_fasta, db_type),\
            "Couldn't format file {0}".format(mock_fasta)

    for file_name in expected_output:
        assert os.path.isfile(os.path.join(
            config.get("paths", "output_db"), "tests", file_name)),\
            "File doesn't exist after format database: {0}".format(
                os.path.join(config.get("paths", "output_db"),
                    file_name))

def setup_blastn():
    utils.format_database("tests/subject.fas", "nucl")

def teardown_blastn():
    config = test_config_file()

    for x in ["subject.fas.nhr", "subject.fas.nin", "subject.fas.nsq"]:
        if os.path.isfile(os.path.join(
            config.get("paths", "output_db"), "tests", x)):
            os.unlink(os.path.join(
                config.get("paths", "output_db"), "tests", x))
    if os.path.isfile(
        os.path.join(config.get("paths", "output_db"), "output.blast")):
        os.unlink(os.path.join(
            config.get("paths", "output_db"), "output.blast"))

@with_setup(setup_blastn, teardown_blastn)
def test_blastn():
    '''Test that blasting of a query against a target is working well'''
    config = test_config_file()
    query = "tests/dna_query.fas"
    subject = "tests/subject.fas"

    assert utils.blastn(query, subject),\
        "Couldn't blast {0} against {1}".format(query, subject)

    expected_output = ["output.blast"]
    for file_name in expected_output:
        assert os.path.isfile(os.path.join(
            config.get("paths", "output_db"), file_name)),\
            "File doesn't exist after blasting: {0}".format(
                os.path.join(config.get("paths", "output_blast"),
                    filename))
        with open(os.path.join(
            config.get("paths", "output_db"), file_name), "r") as output:
            assert output.readlines()[0].split() == ['Mock_DNA_sequence', 'Drosophila', '100.00', '1027', '0', '0', '1', '1027', '237', '1263', '0.0', '1211']

def setup_multicore():
    f_p = open("subject.fas", "w")
    f_p.write("""{0}_1\n{1}{0}_2\n{1}{0}_3\n{1}{0}_4\n{1}""".format(
        ">Core", "TCCTCGATGGGATCGCCACCTTATCGTGGTGAGGGTGTTTGTGTGTCCCAATGACCTCTAGAGCTATGTCGGCGGGAGTATTTTACTCCTGGCAGGGACACCCATGCCGAACAGGTCGAAAGGTAGGGGCCAGACGAAGAGTGATCCACTGGTCCTCCAGGTTGGGGGTTGGGCAAAGGGTTGATAACCCTCTCCCATAAAAAATAGCTTATCACAGAAACCAGAAGCAGAGCAAATTCACTTGGGAAGACCGTGGCTGCATCTCATGAAAGAGATTGTATGACGCGCAGAGGCCAAAGCCATCCGGACGCCCCTGGGCTGACTAAACCATTGGTCCACCCAAAACATGCAATGAGAATAGGTAATTGGAATGTCAGGACATTATATAGTAGCGGCAATG\n"))
    f_p.close()

def teardown_multicore():
    config = test_config_file()

    os.unlink("subject.fas")

    for x in range(4):
        os.unlink(os.path.join(
            config.get("paths", "output_db"), str(x), "subject.fas"))
        os.rmdir(os.path.join(config.get("paths", "output_db"), str(x)))

@with_setup(setup_multicore, teardown_multicore)
def test_multicore():
    '''Test if the multicore is splitting correctly the files'''
    config = test_config_file()
    subject = "subject.fas"

    assert utils.multicore(subject, cores=4),\
        "Couldn't use multicore function"
    for core in range(4):
        assert os.path.isfile(os.path.join(config.get("paths", "output_db"),
            str(core), subject)),\
                "File doesn't exist {0}".format(os.path.join(
                     config.get("paths", "output_db"), str(core), subject))
