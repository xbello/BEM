#!/usr/bin/env/ python
"""Proxy for BLASTing sequences."""

import argparse
import os
from itertools import izip_longest
from multiprocessing import Pool, cpu_count
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

from Bio import SeqIO

import parse


def blastn(query, subject, conf):
    """Return a generator after launching a blastn against a compiled database.

    The generator yields dicts from `parse.blast_tab`, like:

        {'subject_end': '761', 'query_end': '1466', 'e_val': '0.26',
         'query': 'BEL1-I_AG', 'identity': '78.95', 'subject': '3293e',
         'subject_start': '798', 'query_start': '1429', 'length': '38',
         'score': '35.9', 'n_match': '8'}

    """

    binary = os.path.join(
        conf.get("binaries", "blast"),
        conf.get("binaries", "blastn"))

    output_db = conf.get("paths", "output_db")
    input_path = conf.get("paths", "input_path")

    command = [
        binary,
        "-query", os.path.join(input_path, query),
        "-db", os.path.join(input_path, output_db, subject),
        "-outfmt", "6",
        "-task", conf.get("blastn", "task"),
        "-evalue", conf.get("blastn", "evalue"),
        "-word_size", conf.get("blastn", "word"),
        "-penalty", conf.get("blastn", "penalty"),
        "-reward", conf.get("blastn", "reward"),
        "-gapopen", conf.get("blastn", "gapopen"),
        "-gapextend", conf.get("blastn", "gapextend")]

    return parse.blast_tab(run_command(command))


def format_db(fasta_src, db_type, conf):
    """Return the output after formating a database to use with NCBI BLAST.

    db_type is ``nucl`` or ``prot``.

    """

    assert db_type in ["nucl", "prot"]

    binary = conf.get("binaries", "makeblastdb")
    binary_path = conf.get("binaries", "blast")
    output_path = conf.get("paths", "output_db")

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    input_path = conf.get("paths", "input_path")

    command = [
        os.path.join(binary_path, binary),
        "-in", os.path.join(input_path, fasta_src),
        "-out", os.path.join(output_path, fasta_src),
        "-dbtype", db_type]

    return run_command(command)


def run_command(command):
    """Return the output of a command after running it under subprocess."""

    sub = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = sub.communicate()

    if stderr:
        # TODO: Some programs throws common messages through stderr.
        raise IOError(stderr)

    return stdout


def split_query(query_file, n=100):
    """Return a generator of Tempfiles with n seqs each.

    Remember to unlink the pack-file returned, or may get an Exception.

    """

    sequences_iter = [iter(SeqIO.parse(query_file, "fasta"))] * n

    for pack in izip_longest(*sequences_iter):
        yield join_pack(pack)


def join_pack(pack):
    """Yield a pack of sequences."""
    new_fasta = NamedTemporaryFile(delete=False)

    # The last pack comes filled with "None", thus check for its Trueness
    SeqIO.write([p for p in pack if p], new_fasta, "fasta")
    new_fasta.seek(0)

    return new_fasta


if __name__ == "__main__":
    import config

    parser = argparse.ArgumentParser(description="Runs a blast.")
    parser.add_argument("--query", dest="query", required=True)
    parser.add_argument("--subject", dest="subject", required=True)
    parser.add_argument("--strategy", dest="strategy", default="blastn")
    parser.add_argument("--config", dest="config_file")

    args = parser.parse_args()

    config_values = config.get_config_file(args.config_file)

    # Use all available CPUs
    pool = Pool(cpu_count())

    if args.strategy == "blastn":
        format_db(args.subject, "nucl", config_values)
        # Lower the nice value
        os.nice(5)
        # Unset the file_source
        config_values.set("paths", "input_path", "")
        for file_handler in split_query(args.query):
            blastout = blastn(
                file_handler.name, args.subject, config_values)
            # Delete the intermediary Tempfile
            os.unlink(file_handler.name)

    elif args.strategy == "tblastn":
        format_db(args.subject, "prot", config_values)
