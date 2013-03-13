from Bio import SeqIO

import ConfigParser
import os
import subprocess

def blastn(query, subject, evalue="5", penalty="-4", reward="5", gapopen="10",
    gapextend="6"):
    '''Blastn the query sequence against the subject'''
    assert os.path.isfile(query), "{0} not found".format(query)
    assert os.path.isfile(subject), "{0} not found".format(subject)

    config = ConfigParser.RawConfigParser()
    config.read("config.cfg")

    binary = config.get("binaries", "blastn")
    output_path = config.get("paths", "output_db")

    sub = subprocess.Popen([binary,
        "-db", os.path.join(output_path, subject),
        "-query", query,
        "-out", os.path.join(output_path, "output.blast"),
        "-outfmt", "6",
        "-evalue", evalue,
        "-penalty", penalty,
        "-reward", reward,
        "-gapopen", gapopen,
        "-gapextend", gapextend])
    sub.communicate()

    return True

def format_database(fasta_src, db_type):
    '''Format a database to use with NCBI BLAST.
    db_type is nucl or prot'''
    assert db_type in ["nucl", "prot"]

    config = ConfigParser.RawConfigParser()
    config.read("config.cfg")
    binary = config.get("binaries", "makeblastdb")
    output_path = config.get("paths", "output_db")

    sub = subprocess.Popen([binary,
        "-in", fasta_src,
        "-out", os.path.join(output_path, fasta_src),
        "-dbtype", db_type])
    sub.communicate()

    return True

def multicore(subject, cores=1):
    '''Prepare a blast to run in multicore mode.
    The strategy is to divide the subject in as much cores as required,
    putting each subject in a subdir.

    Depends on Biopython library.'''
    config = ConfigParser.RawConfigParser()
    config.read("config.cfg")
    output_path = config.get("paths", "output_db")

    subject_records = SeqIO.parse(open(subject, "r"), "fasta")

    for record in subject_records:
        for core in range(cores):
            if not os.path.isdir(os.path.join(output_path, str(core))):
                os.makedirs(os.path.join(output_path, str(core)))
            file_output = open(os.path.join(
                output_path, str(core), subject), "a")
            file_output.write("{0}\n{1}\n".format(
                record.name, str(record.seq)))
            file_output.close()

    return True
