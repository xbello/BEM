import ConfigParser
import os
import subprocess

def format_database(fasta_src):
    '''Format a database to use with NCBI BLAST'''
    config = ConfigParser.RawConfigParser()
    config.read("config.cfg")
    binary = config.get("binaries", "makeblastdb")
    output_path = config.get("paths", "output_db")

    sub = subprocess.Popen([binary,
        "-in", fasta_src,
        "-out", os.path.join(output_path, fasta_src),
        "-dbtype", "nucl"])
    sub.communicate()

    return True
