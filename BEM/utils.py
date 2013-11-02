from Bio import SeqIO

import ConfigParser
import os
import subprocess

def blastn(query, subject, config, evalue="5", penalty="-4", reward="5",
    gapopen="10", gapextend="6", word="11"):
    '''Blastn the query sequence against the subject'''
    binary_path = config.get("binaries", "blast")
    binary = config.get("binaries", "blastn")
    output_db = config.get("paths", "output_db")
    output_blast = config.get("paths", "output_blast")

    if not os.path.isdir(output_blast):
        os.makedirs(output_blast)

    input_path = config.get("paths", "input_path")

    assert os.path.isfile(os.path.join(input_path, query)),\
        "{0} not found".format(query)
    assert os.path.isfile(os.path.join(input_path, subject)),\
        "{0} not found".format(subject)

    command = [os.path.join(binary_path, binary),
        "-db", os.path.join(output_db, subject),
        "-query", os.path.join(input_path, query),
        "-out", os.path.join(output_blast, "{0}.blast".format(subject)),
        "-outfmt", "6",
        "-evalue", evalue,
        "-word_size", word,
        "-penalty", penalty,
        "-reward", reward,
        "-gapopen", gapopen,
        "-gapextend", gapextend]

    sub = subprocess.Popen(command)
    sub.communicate()

    return command

def format_database(fasta_src, db_type, config):
    '''Format a database to use with NCBI BLAST.
    db_type is nucl or prot'''
    assert db_type in ["nucl", "prot"]

    binary = config.get("binaries", "makeblastdb")
    binary_path = config.get("binaries", "blast")
    output_path = config.get("paths", "output_db")
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    input_path = config.get("paths", "input_path")

    command = [os.path.join(binary_path, binary),
        "-in", os.path.join(input_path, fasta_src),
        "-out", os.path.join(output_path, fasta_src),
        "-dbtype", db_type]

    sub = subprocess.Popen(command, stdout=subprocess.PIPE)
    sub.communicate()

    return command

def multicore(subject, config, cores=1):
    '''Prepare a blast to run in multicore mode.
    The strategy is to divide the subject in as much cores as required,
    putting each subject in a subdir.

    Depends on Biopython library.'''
    output_path = config.get("paths", "output_db")
    input_path = config.get("paths", "input_path")

    subject_records = SeqIO.parse(
        open(os.path.join(input_path, subject), "r"), "fasta")

    created_subjects = []
    core = 0
    for record in subject_records:
        target_dir = os.path.join(output_path, str(core))
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        file_path = os.path.join(target_dir, subject)

        if file_path not in created_subjects:
            created_subjects.append(file_path)

        mode = ("a" if os.path.isfile(file_path) else "w")

        file_output = open(file_path, mode)
        file_output.write(">{0}\n{1}\n".format(
            record.name, str(record.seq)))
        file_output.close()
        
        core = ((core + 1) if core < (cores - 1) else 0)

    return created_subjects
